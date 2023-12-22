import io
from .xyzgeneric import *

# Default functions for loading and saving files
_loadfunc = lambda byteio : byteio.read().decode(encoding="utf-8").rstrip()

_savefunc = lambda filename, val : print(val, file=open(filename,"w"))

class XYZTxt(XYZGeneric):
    def __init__(self, base, loadfunc=_loadfunc, savefunc=_savefunc, **kwargs):
        super().__init__(base, loadfunc=loadfunc, savefunc=savefunc, **kwargs)

class XYZHttpTxt(XYZHttpGeneric):
    def __init__(self, base, loadfunc=_loadfunc, **kwargs):
        super().__init__(base, loadfunc=_loadfunc, **kwargs)

# {"type string from the extension" : Class}
xyztiletype = {"txt":XYZTxt}
xyzhttptype = {"txt":XYZHttpTxt}
