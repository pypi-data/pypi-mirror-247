import numpy as np
import xarray as xr
from xgcm import Grid

ds = xr.Dataset(
    coords={
        "x_c": (
            ["x_c"],
            np.arange(1, 10),
        ),
        "x_g": (
            ["x_g"],
            np.arange(0.5, 9),
        ),
    }
)
grid = Grid(
    ds, coords={"X": {"center": "x_c", "left": "x_g"}}, autoparse_metadata=False
)
da = np.sin(ds.x_c * 2 * np.pi / 9)
grid.interp(da, axis="X")


era = xr.open_dataset("../era5_2021/FloodCase_202107_ml_T.nc")
Grid(era)

erapl = xr.open_dataset("../era5_2021/FloodCase_202107_q.nc")
Grid(erapl, periodic=False, boundary="extend")


ds = xr.Dataset(
    coords={
        "xc": (
            ["xc"],
            np.arange(1, 10),
        ),
        "xl": (
            ["xl"],
            np.arange(0.5, 9),
        ),
    }
)


xr.DataArray()
