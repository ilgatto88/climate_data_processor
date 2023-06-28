import xarray as xr


def convert_dataset_to_geotiff(dataset: xr.Dataset, output_path: str) -> None:
    """
    Converts an xarray Dataset to GeoTIFF format and saves it to
    the specified output path.
    """
    dataset.rio.to_raster(output_path)


def concatenate_dictionaries(dictionary_list: list[dict]) -> dict:
    """This function converts a list of dictionaries into a JSON object."""
    dicts = {}
    for d in dictionary_list:
        for k, v in d.items():
            dicts[k] = v

    return dicts
