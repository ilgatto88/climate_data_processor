import pandas as pd


def add_oeks_statistics(data: pd.DataFrame) -> pd.DataFrame:
    model_median = data.median(axis=1)
    model_mean = data.mean(axis=1)
    model_10perc = data.quantile(q=0.1, axis=1)
    model_90perc = data.quantile(q=0.9, axis=1)
    model_min = data.min(axis=1)
    model_max = data.max(axis=1)

    data["minimum"] = model_min
    data["lowerPercentile"] = model_10perc
    data["median"] = model_median
    data["mean"] = model_mean
    data["upperPercentile"] = model_90perc
    data["maximum"] = model_max

    data = data.round(decimals=1)

    data.reset_index(inplace=True, names="Year")
    return data
