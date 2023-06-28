import xarray as xr

from api_data_processing import (
    config,
    format_conversion,
    general,
    geodataframe_tools,
    loaders,
)


def oeks_to_geotiff_modelwise_and_aggr(source: str) -> None:
    """Creates 1991-2020 mean temperature for AT for each model from RCP2.6 (geotiff)"""
    data = loaders.load_dataset(source)
    data_selected_time = data.sel(time=slice(TS_START, TS_END))
    dataarray_aggr = general.calculate_along_dimension(
        data_selected_time["tm"], "time", xr.DataArray.mean
    )

    for n in range(len(dataarray_aggr["realization"])):
        print(f"Processing {dataarray_aggr[n,:,:]['realization'].values}")
        dataset = dataarray_aggr[n, :, :].to_dataset(name="tm")
        outname = f"{config.BASE_DATA_PATH}geotif/oeks_rcp26_model_{n}_AT_9120.tif"
        format_conversion.convert_dataset_to_geotiff(dataset, outname)

    # create 1991-2020 mean temperature for AT as model mean from RCP2.6 (geotiff)
    print("Processing model mean for 1991-2020 for AT from OEKS RCP2.6")
    dataarray_aggr_models = general.calculate_along_dimension(
        dataarray_aggr, "realization", xr.DataArray.mean
    )
    outname = f"{config.BASE_DATA_PATH}geotif/rcp26/oeks_rcp26_model_mean_AT_9120.tif"
    format_conversion.convert_dataset_to_geotiff(
        dataarray_aggr_models.to_dataset(name="tm"), outname
    )

    # Creates 1991-2020 mean temperature for AT as model median from RCP2.6 (geotiff)
    print("Processing model median for 1991-2020 for AT from OEKS RCP2.6")
    dataarray_aggr_models = general.calculate_along_dimension(
        dataarray_aggr, "realization", xr.DataArray.median
    )
    outname = f"{config.BASE_DATA_PATH}geotif/rcp26/oeks_rcp26_model_median_AT_9120.tif"
    format_conversion.convert_dataset_to_geotiff(
        dataarray_aggr_models.to_dataset(name="tm"), outname
    )


if __name__ == "__main__":
    # to execute this script, use ./manage.py shell < preprocessing/process_oeks_data.py
    # user config
    TS_START = "1991-01-01"
    TS_END = "2020-01-01"
    input_file = f"{config.BASE_DATA_PATH}netcdf/oeks-rcp26-tm-austria-YS.nc"
    shapefile_path = config.MUNICIPALITY_SHAPEFILE
    geodf = geodataframe_tools.load_shapefile(shapefile_path)
