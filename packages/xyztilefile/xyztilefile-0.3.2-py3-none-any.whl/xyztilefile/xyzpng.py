import json
from skimage import io as skiio
from .xyzgeneric import *

# Default functions for loading and saving files
_loadfunc = lambda byteio : skiio.imread(byteio)

_savefunc = lambda filename, val : skiio.imsave(filename, val, plugin='imageio')

class XYZPng(XYZGeneric):
    def __init__(self, base, loadfunc=_loadfunc, savefunc=_savefunc, **kwargs):
        super().__init__(base, loadfunc=loadfunc, savefunc=savefunc, **kwargs)

class XYZHttpPng(XYZHttpGeneric):
    def __init__(self, base, loadfunc=_loadfunc, **kwargs):
        super().__init__(base, loadfunc=_loadfunc, **kwargs)


# {"type string from the extension" : Class}
xyztiletype = {"png":XYZPng}
xyzhttptype = {"png":XYZHttpPng}
