import dataclasses
import functools
from typing import *

import torch
from torch.distributed import ProcessGroup

from . import _codecs as codecs
from ._codecs import Codec
from ._utils import div_round_up


class Waitable(Protocol):
    """An object you can call wait() on.

    Meaning varies. Mostly for typing.
    """

    def wait(self) -> None:
        ...


@dataclasses.dataclass
class SimpleFuture:
    callback: Callable

    def wait(self) -> None:
        self.callback()


def _default_compressed_allgather_codec(clip_min: float,
                                        clip_max: float) -> Codec:
    return codecs.SequentialCodec([
        codecs.LambdaCodec(
            functools.partial(torch.nan_to_num, neginf=0, posinf=0)),
        codecs.LambdaCodec(
            functools.partial(torch.clip, min=clip_min, max=clip_max)),
        codecs.SignedIntQuantizer(num_bits=8, pad_encode_to_bytes=16)
    ])


_patched_allgather_process_groups = []  # TODO no global var...somehow
_raw_allgather_base = ProcessGroup._allgather_base


def patch_allgathers(pg: Optional[ProcessGroup] = None,
                     codec: Optional[Codec] = None,
                     clip_abs_threshold: float = 4) -> None:
    if codec is None:
        if clip_abs_threshold <= 0:
            raise ValueError('clip_abs_threshold must be > 0 if no codec' +
                             f'is provided; got {clip_abs_threshold}')
        codec = _default_compressed_allgather_codec(
            clip_min=-clip_abs_threshold, clip_max=clip_abs_threshold)

    global _patched_allgather_process_groups

    if pg is not None:
        _patched_allgather_process_groups.append(pg)

    # TODO should really just have a compressed allgather func and then
    # partially bind it + monkey patch it in
    @functools.wraps(ProcessGroup._allgather_base)
    def _allgather_base(pg_self: ProcessGroup,
                        out_tensor: torch.Tensor,
                        in_tensor: torch.Tensor,
                        *args,
                        _codec: Optional[Codec] = codec,
                        **kwargs):

        # just behave normally if this isn't a group we wanted to patch
        if pg_self not in _patched_allgather_process_groups:
            return _raw_allgather_base(pg_self, out_tensor, in_tensor, *args,
                                       **kwargs)

        in_compressed = _codec.encode(in_tensor)
        num_ranks = out_tensor.numel() // in_tensor.numel()
        out_bytes_per_in_byte = (out_tensor.element_size() //
                                 in_compressed.element_size())
        out_compressed_numel = num_ranks * in_compressed.numel()
        out_compressed = torch.empty(out_compressed_numel,
                                     dtype=in_compressed.dtype,
                                     device=in_compressed.device)

        handle: Optional[Waitable] = _raw_allgather_base(
            pg_self, out_compressed, in_compressed, *args, **kwargs)

        # decompression callback to run after the async call waits
        def _copy_into_output(_out_compressed: torch.Tensor = out_compressed,
                              _out_raw: torch.tensor = out_tensor,
                              _num_chunks: int = num_ranks,
                              _codec: Codec = _codec,
                              _handle: Optional[Waitable] = handle):
            if _handle is not None:
                handle.wait()
            _out_compressed = _out_compressed.view(_num_chunks, -1)
            _out_raw = _out_raw.view(_num_chunks, -1)
            for c in range(_num_chunks):  # TODO batched decompression kernel
                _codec.decode(_out_compressed[c], out=_out_raw[c])

        if handle is None:
            _copy_into_output()
        else:
            return SimpleFuture(callback=_copy_into_output)

    ProcessGroup._allgather_base = _allgather_base
