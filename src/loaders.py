import xarray as xr

import static_geo


def load_dataset(path: str) -> xr.Dataset:
    """Load eiter OEKS or Spartacus dataset"""
    dataset = xr.open_dataset(filename_or_obj=path, engine="netcdf4")
    if "spartacus" in path:
        dataset = dataset.sel(y=dataset.y[::-1])
    elif "oeks" in path:
        pass
    else:
        raise ValueError("Unknow source of data")

    dataset = dataset.drop_vars("time_bnds")
    if dataset.attrs.get("grid_mapping") is not None:
        del dataset.attrs["grid_mapping"]

    dataset.rio.write_crs(static_geo.EPSG_LCC, inplace=True)
    return dataset
