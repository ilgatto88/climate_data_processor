import geopandas
import xarray as xr

import area_selection
import config
import general
from models import MunicipalityDataSettings


def preprocess_historical_data(
    dataset: xr.Dataset,
    settings: MunicipalityDataSettings,
    area_geodataframe: geopandas.GeoDataFrame,
) -> xr.DataArray:
    """Loads the historical data and cuts it to the selected area."""
    area_data = area_selection.reduce_area(
        dataset, settings.climateParameter, area_geodataframe
    )
    return area_data


def create_historical_raw_data(
    preprocessed_data: xr.DataArray,
) -> dict[str, list[float]]:
    raw_data = [round(float(value), 1) for value in preprocessed_data.values]
    return {"rawData": raw_data}


def create_historical_statistics(preprocessed_data: xr.DataArray) -> dict[str, dict]:
    statistics_dictionaries = {}
    for period in config.STATISTIC_PERIODS_HISTORICAL:
        period_data = create_historical_0d_stats(
            preprocessed_data, period[0], period[1]
        )
        statistics_dictionaries.update(period_data)

    return {"statistics0D": statistics_dictionaries}


def create_historical_0d_stats(data: xr.DataArray, start: str, end: str):
    period_key = f"{start}-{end}"
    rounding_decimals = 1

    period_data = data.sel(time=slice(f"{start}-01-01", f"{end}-01-01"))
    historical_mean = general.calculate_along_dimension(
        period_data, "time", xr.DataArray.mean
    )

    # put values into a dictionary and round them
    statistics = {}
    statistics[period_key] = {}
    statistics[period_key]["mean"] = float(historical_mean.values)

    return general.round_dict_values(statistics, rounding_decimals)
