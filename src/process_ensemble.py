import geopandas
import pandas as pd
import xarray as xr

from api_data_processing import (
    area_selection,
    config,
    data_statistics,
    general,
    loaders,
)
from api_data_processing.models import MunicipalityDataSettings


def preprocess_ensemble_data(
    settings: MunicipalityDataSettings,
    scenario: str,
    area_geodataframe: geopandas.GeoDataFrame,
) -> xr.DataArray:
    data = loaders.load_dataset(settings.create_future_input_file_path(scenario))
    area_data = area_selection.reduce_area(
        data, settings.climateParameter, area_geodataframe
    )
    return area_data


def oeks_1d_data_pipeline(preprocessed_data: xr.DataArray) -> pd.DataFrame:
    columns = preprocessed_data.realization.values
    index = list(range(config.ENSEMBLE_START_YEAR, config.ENSEMBLE_END_YEAR + 1))
    data_as_dataframe = pd.DataFrame(
        preprocessed_data, index=columns, columns=index
    ).transpose()
    return data_statistics.add_oeks_statistics(data_as_dataframe)


def oeks_0d_data_pipeline(
    preprocessed_data: xr.DataArray,
) -> dict[str, dict[str, float]]:
    statistics_dictionaries = {"statistics0D": {}}
    for period in config.STATISTIC_PERIODS_OEKS:
        period_data = create_oeks_0d_stats(preprocessed_data, period[0], period[1])
        statistics_dictionaries["statistics0D"].update(period_data)

    return statistics_dictionaries


def create_oeks_0d_stats(data: xr.DataArray, start: str, end: str):
    period_key = f"{start}-{end}"
    stat_dim = "realization"
    rounding_decimals = 1

    period_data = data.sel(time=slice(f"{start}-01-01", f"{end}-01-01"))
    data_1d = general.calculate_along_dimension(period_data, "time", xr.DataArray.mean)

    # calculate statistics
    model_min = data_1d.min(dim=stat_dim, keep_attrs=False, skipna=True)
    model_lower_percentile = data_1d.quantile(
        q=0.1, dim=stat_dim, keep_attrs=False, skipna=True
    )
    model_mean = data_1d.mean(dim=stat_dim, keep_attrs=False, skipna=True)
    model_median = data_1d.median(dim=stat_dim, keep_attrs=False, skipna=True)
    model_upper_percentile = data_1d.quantile(
        q=0.9, dim=stat_dim, keep_attrs=False, skipna=True
    )
    model_max = data_1d.max(dim=stat_dim, keep_attrs=False, skipna=True)

    # put values into a dictionary and round them
    statistics = {}
    statistics[period_key] = {}
    statistics[period_key]["minimum"] = float(model_min.values)
    statistics[period_key]["lowerPercentile"] = float(model_lower_percentile.values)
    statistics[period_key]["median"] = float(model_mean.values)
    statistics[period_key]["mean"] = float(model_median.values)
    statistics[period_key]["upperPercentile"] = float(model_upper_percentile.values)
    statistics[period_key]["maximum"] = float(model_max.values)

    return general.round_dict_values(statistics, rounding_decimals)
