import os
from .xyztilefile import *

class XYZTileManager:
    """Utilize locally saved cache files with the source

    The source can be local or online.
    Firstly, this class try to load from local cache file.
    If there is no cache file, this class retrieves data from the source.
    The retrieve data is automatically saved to local cache file.

    """
    def __init__(self, srcbase:str, cachebase:str, **kwargs):
        self._cache = {}
        self._src = XYZTileFile(srcbase, cache=self._cache, **kwargs)
        self._lcl = XYZHttpTileFile(cachebase, cache=self._cache, **kwargs)

    def get(self, x:int, y:int, z:int):
        try:
            return self._lcl.get(x,y,z)
        except OSError:
            pass
        res = self._src.get(x,y,z)
        print(self._lcl)
        self._lcl.save(x,y,z)
        return res

    def __repr__(self):
        return f"<{repr(self.__class__)}: {repr(self._src)}, {repr(self._lcl)}>"
