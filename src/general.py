import numbers
from typing import Callable, Union

import numpy as np
import pandas as pd
import xarray as xr


def remove_dimension(dataset: xr.Dataset, dimension: str) -> xr.Dataset:
    """Removes the specified dimension from the given xarray Dataset."""
    return dataset.squeeze(dim=dimension)


def calculate_along_dimension(
    dataarray: xr.DataArray,
    dimension: Union[str, list[str]],
    func: (Callable[[xr.DataArray, str], xr.DataArray]),
    **kwargs,
) -> xr.DataArray:
    """
    Calculates the aggregation along the specified dimension using the
    provided function.

    Examples for the func parameter:
    - xr.Dataarray.mean
    - xr.Dataarray.median
    - ...
    """
    if func == xr.DataArray.quantile:
        quantile_value = kwargs["q"]
        return dataarray.quantile(
            q=quantile_value, dim=dimension, keep_attrs=False, skipna=True
        )
    return func(dataarray, dim=dimension, keep_attrs=False, skipna=True)  # type: ignore


def prepare_array_for_json(values: pd.Series, decimals: int = 1) -> list:
    """
    This function prepares a pandas Series for JSON serialization by converting
    it to a list, rounding the values to the specified number of decimals, and
    replacing any NaN values with None.
    """
    values = values.to_list()  # type: ignore
    rounded_values = [round(value, decimals) for value in values]
    return [None if np.isnan(value) else value for value in rounded_values]


def round_dict_values(data: dict, decimals: int):
    if isinstance(data, dict):
        return {key: round_dict_values(value, decimals) for key, value in data.items()}
    elif isinstance(data, numbers.Real):
        return round(data, decimals)
    else:
        return data
