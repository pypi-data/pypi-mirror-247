import os
import math
import requests
from .xyzgeneric import *

__LATLIMIT = 85.0511
__YZERO = math.atanh(math.sin(math.radians(__LATLIMIT)))
__TD = 256

def calc_xyz_from_lonlat(lon: float, lat: float, z: int):
    """Calculates XYZ tile indices of the given zoom level at the given longitude and latitude.

    Args:
        lon (float): longitude (degree).
        lat (float): latitude (degree).
        z (int): zoom level (0 or greater).

    Returns:
        (x, y, z) (tupple): tile indices x and y of the zoom level z.

    """
    if z < 0:
        raise ValueError("Zoom level must be 0 or greater.")
    #print(lon, lat, z)
    n = 2.0 ** z
    x = int((lon + 180.0) / 360.0 * n)
    y = int( (__YZERO-math.atanh(math.sin(math.radians(lat))))
        /(2.0*__YZERO) * n )
    return (x, y, z)

def calc_lonlat_from_xyz(x:int, y:int, z:int):
    """Calculates (lon, lat) degrees of the north west corner of the tile
    """
    n = 2.0 ** z
    lon_deg = x / n * 360.0 - 180.0
    ycorr = __YZERO - (y * __YZERO * 2.0 / n)
    lat_rad = math.asin(math.tanh(ycorr))
    lat_deg = math.degrees(lat_rad)
    return lon_deg, lat_deg


def calc_bounds_xyz(x:int, y:int, z:int):
    """Calculates the bounds (west, south, east, north) of the tile
    """
    west, north = calc_lonlat_from_xyz(x, y, z)
    east, south = calc_lonlat_from_xyz(x+1, y+1, z)
    return west, south, east, north

class XYZTileFile:
    """Factory class of XYZFiletype instances.

    An instance of the appropriate XYZFiletype class will be returned by judging the extension of the given base string. This class will call XYZHttpTileFile constructor if the base start with "http://".

    Args:
        base (string): base url or file path of xyz file system. This must contain keywords "{x}", "{y}", and "{z}".

    Optional Keyargs:
        loadfunc (method): (optional) user-defined loading function.
        savefunc (method): (optional) user-defined saving function.

    """
    typeclass = {"generic":XYZGeneric}
    def __new__(cls, base: str, type=None, **kwargs):
        if isinstance(base, str):
            if base[0:7] == "http://" or base[0:8] == "https://":
                return XYZHttpTileFile(base, **kwargs)
            if type in cls.typeclass: # try user-specified type
                return cls.typeclass[type](base, **kwargs)
            type = os.path.splitext(base)[-1][1:]
            if type in cls.typeclass:
                return cls.typeclass[type](base, **kwargs)
        return XYZGeneric(base=base, **kwargs)

class XYZHttpTileFile(XYZTileFile):
    """Factory class of XYZHttpFiletype instances.

    An instance of the appropriate XYZHttpFiletype class will be returned by judging the extension of the given base string. This class assumes that the base starts with "http://".

    Args:
        base (string): base url or file path of xyz file system. This must contain keywords "{x}", "{y}", and "{z}".

    Optional Keyargs:
        loadfunc (method): (optional) user-defined loading function.
        savefunc (method): (optional) user-defined saving function.

    """
    typeclass = {"generic":XYZHttpGeneric}
    def __new__(cls, base: str, type=None, **kwargs):
        if isinstance(base, str):
            if base[0:7] != "http://" and base[0:8] != "https://":
                return XYZTileFile(base, **kwargs)
            if type in cls.typeclass:
                return cls.typeclass[type](base, **kwargs)
            type = os.path.splitext(base)[-1][1:]
            if type in cls.typeclass:
                return cls.typeclass[type](base, **kwargs)
        return XYZHttpGeneric(base=base, **kwargs)


for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module == "xyztilefile.py" \
        or module == "xyzgeneric.py" or module[-3:] != '.py':
        continue
    #print(f"Importing {module}")
    exec(f"from .{module[:-3]} import *" )
    XYZTileFile.typeclass.update(xyztiletype)
    XYZHttpTileFile.typeclass.update(xyzhttptype)
del module
del xyztiletype
del xyzhttptype

#print(XYZTileFile.typeclass)
