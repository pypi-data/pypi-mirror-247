import typing
from ..error import VLPValueError as VLPValueError
from _typeshed import Incomplete

class BandFilter:
    N: Incomplete
    Fs: Incomplete
    T: Incomplete
    t: Incomplete
    fftfreq: Incomplete
    fm: Incomplete
    W: Incomplete
    window_fft: Incomplete
    window: Incomplete
    def __init__(self, n, fs, fm, w: int = ..., *args, **kwargs) -> None: ...
    def filter(self, signal): ...

class BaseFilter:
    Fc: Incomplete
    Fs: Incomplete
    Wp: Incomplete
    Ws: Incomplete
    btype: Incomplete
    analog: Incomplete
    def __init__(self, fc, fs, D: list = ..., G: list = ..., btype: str = ..., analog: bool = ..., *args, **kwargs) -> None: ...
    def show_wave(self, N, whole: bool = ..., savepath=..., showfig: bool = ...) -> None: ...
    def filter(self, x, lfilter: bool = ...): ...

class ButterFilter(BaseFilter):
    def __init__(self, fc, fs, D: list = ..., G: list = ..., btype: str = ..., analog: bool = ..., *args, **kwargs) -> None: ...

class ChebyFilter(BaseFilter):
    def __init__(self, fc, fs, D: list = ..., G: list = ..., btype: str = ..., analog: bool = ..., cheby: int = ..., *args, **kwargs) -> None: ...

class EllipFilter(BaseFilter):
    def __init__(self, fc, fs, D: list = ..., G: list = ..., btype: str = ..., analog: bool = ..., *args, **kwargs) -> None: ...

class BesselFilter(BaseFilter):
    def __init__(self, fc, fs, n, Wn: typing.Union[int, list], btype: str = ..., analog: bool = ..., *args, **kwargs) -> None: ...

class FIR_Filter(BaseFilter):
    def __init__(self, fc, fs, n, Wp, window: str = ..., btype: str = ..., *args, **kwargs) -> None: ...
