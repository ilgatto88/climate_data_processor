import pandas as pd

import config
from general import prepare_array_for_json
from models import MunicipalityDataSettings


def create_municipality_meta_dict(meta: MunicipalityDataSettings) -> dict:
    return {
        "meta": {
            "municipalityId": meta.municipalityId,
            "climateParameter": meta.climateParameter,
            "temporalResolution": meta.temporal_resolution,
            "analysisTimeRange": list(
                range(meta.analysis_start_year, meta.analysis_end_year + 1)
            ),
            "ensembleTimeRange": list(
                range(meta.ensemble_start_year, meta.ensemble_end_year + 1)
            ),
        }
    }


def create_historical_data_dict() -> dict:
    return {"historical": {"analysisModel": "Spartacusv2.1"}}


def create_ensemble_data_dict(data: pd.DataFrame) -> dict:
    models = [x for x in data if x not in config.STATISTICS + ["Year"]]
    model_raw_data = {}
    for model in models:
        model_raw_data[model] = prepare_array_for_json(data[model])
    return {
        "modelNames": models,
        "rawData": model_raw_data,
        "statistics1D": {
            "minimum": prepare_array_for_json(data["minimum"]),
            "lowerPercentile": prepare_array_for_json(data["lowerPercentile"]),
            "median": prepare_array_for_json(data["median"]),
            "mean": prepare_array_for_json(data["mean"]),
            "upperPercentile": prepare_array_for_json(data["upperPercentile"]),
            "maximum": prepare_array_for_json(data["maximum"]),
        },
    }
