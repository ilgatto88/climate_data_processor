import gc
import json

import xarray as xr

from src import (
    config,
    create_data_dictionaries,
    format_conversion,
    geodataframe_tools,
    process_ensemble,
    process_historical,
)
from src.loaders import load_dataset
from src.models import MunicipalityDataSettings


def create_municipality_climate_data(
    settings: MunicipalityDataSettings, historical_data: xr.Dataset
) -> dict:
    area_geodataframe = settings.load_geodataframe()

    # Meta data
    meta_dict = create_data_dictionaries.create_municipality_meta_dict(settings)

    # Historical data
    preprocessed_historical_data = process_historical.preprocess_historical_data(
        historical_data, settings, area_geodataframe
    )

    historical_dict = create_data_dictionaries.create_historical_data_dict()
    historical_dict["historical"].update(
        process_historical.create_historical_raw_data(preprocessed_historical_data)
    )
    historical_dict["historical"].update(
        process_historical.create_historical_statistics(preprocessed_historical_data)
    )

    # Ensemble data
    ensemble_dict = {"ensemble": {}}

    for scenario in ["rcp26", "rcp85"]:
        preprocessed_ensemble_data = process_ensemble.preprocess_ensemble_data(
            settings, scenario, area_geodataframe
        )
        ensemble_dict["ensemble"].update({scenario: {}})

        ensemble_dict["ensemble"][scenario].update(
            create_data_dictionaries.create_ensemble_data_dict(
                process_ensemble.oeks_1d_data_pipeline(preprocessed_ensemble_data)
            )
        )

        ensemble_dict["ensemble"][scenario].update(
            process_ensemble.oeks_0d_data_pipeline(preprocessed_ensemble_data)
        )

    climate_data_dict = format_conversion.concatenate_dictionaries(
        [meta_dict, historical_dict, ensemble_dict]
    )

    return climate_data_dict


if __name__ == "__main__":
    shape = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)

    PARAMETER = "tm"
    TEMPORAL_RESOLUTION = "annual"

    municipality_list = json.load(
        open(
            f"{config.BASE_DATA_PATH}metadata/json/municipalities.json",
            "r",
        )
    )

    historical_data = load_dataset(
        (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/historical/"
            f"spartacus-{PARAMETER}-austria-YS.nc"
        )
    )

    municipality_data_list = []

    for municipality in municipality_list:
        municipality_settings = MunicipalityDataSettings(
            municipalityId=municipality["m_id"],
            climateParameter=PARAMETER,
            temporal_resolution=TEMPORAL_RESOLUTION,
            analysis_start_year=config.ANALYSIS_START_YEAR,
            analysis_end_year=config.ANALYSIS_END_YEAR,
            ensemble_start_year=config.ENSEMBLE_START_YEAR,
            ensemble_end_year=config.ENSEMBLE_END_YEAR,
            shape=shape,
        )

        print(f"Processing {municipality_settings.municipalityId}")

        data = create_municipality_climate_data(municipality_settings, historical_data)
        municipality_data_list.append(data)
        gc.collect()

    json.dump(
        municipality_data_list,
        open(
            f"{config.BASE_DATA_PATH}climate_data/json/municipality_data_{PARAMETER}2.json",
            "w",
        ),
    )
