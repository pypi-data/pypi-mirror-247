import pickle
from .xyzgeneric import *

# Default functions for loading and saving files
_loadfunc = lambda byteio : pickle.load(byteio)

_savefunc = lambda filename, val : pickle.dump(val, open(filename,"wb"))

class XYZPickle(XYZGeneric):
    def __init__(self, base, loadfunc=_loadfunc, savefunc=_savefunc, allow_pickle=False, **kwargs):
        if not allow_pickle:
            raise RuntimeError("The pickle module is not secure. Only unpickle data you trust.\nIt is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never unpickle data that could have come from an untrusted source, or that could have been tampered with.\nWith trusted data source, set allow_pickle to True at the initialization of XYZTileFile.")
        super().__init__(base, loadfunc=loadfunc, savefunc=savefunc, **kwargs)

class XYZHttpPickle(XYZHttpGeneric):
    def __init__(self, base, loadfunc=_loadfunc, **kwargs):
        raise NotImplementedError("Pickle is not allowed on XYZTileFile with HTTP due to security reasons.")


# {"type string from the extension" : Class}
xyztiletype = {"pickle":XYZPickle,"pkl":XYZPickle}
xyzhttptype = {"pickle":XYZHttpPickle,"pkl":XYZHttpPickle}
