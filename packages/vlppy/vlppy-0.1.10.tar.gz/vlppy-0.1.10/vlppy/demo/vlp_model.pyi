from ..model import LED as LED, PD as PD, Room as Room
from _typeshed import Incomplete

class VLP_Model:
    room: Incomplete
    pd1: Incomplete
    pd2: Incomplete
    pd3: Incomplete
    pd4: Incomplete
    t: Incomplete
    led1: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def get_data(self): ...
    def show(self, z, savepath=..., showfig: bool = ...) -> None: ...
