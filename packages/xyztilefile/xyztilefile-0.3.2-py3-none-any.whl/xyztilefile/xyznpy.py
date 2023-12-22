import numpy as np
from .xyzgeneric import *

# Default functions for loading and saving files
_loadfunc = lambda byteio : np.load(byteio)

_savefunc = lambda filename, val : np.save(filename,val)

class XYZNpy(XYZGeneric):
    def __init__(self, base, loadfunc=_loadfunc, savefunc=_savefunc, **kwargs):
        super().__init__(base, loadfunc=loadfunc, savefunc=savefunc, **kwargs)

class XYZHttpNpy(XYZHttpGeneric):
    def __init__(self, base, loadfunc=_loadfunc, **kwargs):
        super().__init__(base, loadfunc=_loadfunc, **kwargs)

# {"type string from the extension" : Class}
xyztiletype = {"npy":XYZNpy}
xyzhttptype = {"npy":XYZHttpNpy}
