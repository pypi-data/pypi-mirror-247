import warnings
import os
import io
import requests
import copy

# Default functions for loading and saving files
_loadfunc = lambda byteio : byteio.read()

_savefunc = lambda filename, val : print(filename, val)

class XYZGeneric:
    def __init__(self, base: str, loadfunc=_loadfunc, savefunc=_savefunc, cache=None):
        if not isinstance(base, str):
            raise TypeError("base must be string.")
        if not ("{x}" in base and "{y}" in base and "{z}" in base):
            raise ValueError('base must contain "{x}", "{y}", and "{z}".')
        self._base = base
        self._keyfmt = "{z}/{x}/{y}"
        self._loadfunc = loadfunc
        if loadfunc is _loadfunc:
            warnings.warn("XYZGeneric: default loading function is set.")
        self._savefunc = savefunc
        if savefunc is _savefunc:
            warnings.warn("XYZGeneric: default saving function is set.")
        self.clc(cache=cache)

    def __repr__(self):
        # ref: https://ja.pymotw.com/2/pprint/
        return f"<{repr(self.__class__)}: base={repr(self._base)}, cache={repr(self._cache)}>"

    def has(self, x:int, y:int, z:int):
        key = self._keyfmt.format(x=x,y=y,z=z)
        return key in self._base

    def get(self, x:int, y:int, z:int):
        key = self._keyfmt.format(x=x,y=y,z=z)
        if key not in self._base:
            with open(self._base.format(x=x,y=y,z=z), "rb") as ifile:
                self._cache[key] = self._loadfunc(ifile)
        return copy.deepcopy(self._cache[key])

    def set(self, x:int, y:int, z:int, val):
        key = self._keyfmt.format(x=x,y=y,z=z)
        self._cache[key] = val
        return self

    def save(self, x:int, y:int, z:int):
        key = self._keyfmt.format(x=x,y=y,z=z)
        #print(key)
        if key not in self._cache:
            return False
        path = self._base.format(x=x,y=y,z=z)
        dir = os.path.dirname(path)
        print(f"Saving check : {dir} : {os.path.exists(dir)}")
        if not os.path.exists(dir):
            os.makedirs(dir)
        self._savefunc(path, self._cache[key])
        return True

    def set_save(self, x:int, y:int, z:int, val):
        self.set(self, x, y, z, val)
        return self.save(self, x, y, z)

    def save_all(self):
        for key in self._cache:
            dir = os.path.dirname(key)
            if not os.path.exists(dir):
                os.makedirs(dir)
            self._savefunc(key, self._cache[key])
        return True

    def clc(self, cache=None):
        if cache is None:
            cache = {}
        if not isinstance(cache, dict):
            raise TypeError("chache must be dict.")
        if len(cache) > 0:
            warnings.warn("XYZGeneric: non-empty shared chache is set.")
        self._cache = cache

class XYZHttpGeneric(XYZGeneric):
    def __init__(self, base, loadfunc=_loadfunc, **kwargs):
        super().__init__(base, loadfunc=loadfunc, savefunc=None, **kwargs)

    def get(self, x:int, y:int, z:int):
        key = self._keyfmt.format(x=x,y=y,z=z)
        if key not in self._base:
            res = requests.get(self._base.format(x=x,y=y,z=z))
            if res.status_code != 200:
                res.raise_for_status()
                #raise OSError(f"Failed to fetch {key}")
            self._cache[key] = self._loadfunc(io.BytesIO(res.content))
        #copy.deepcopy した方がいい？
        return copy.deepcopy(self._cache[key])


    def set(self, *args, **kwargs):
        raise NotImplementedError("set is nulled for http tile class.")

    def save(self, *args, **kwargs):
        raise NotImplementedError("save is nulled for http tile class.")

    def save_all(self, *args, **kwargs):
        raise NotImplementedError("save_all is nulled for http tile class.")


# {"type string from the extension" : Class}
# These variables are not used for Generic classes
#xyztiletype = {"xyzgeneric":XYZGeneric}
#xyzhttptype = {"xyzgeneric":XYZHttpGeneric}
