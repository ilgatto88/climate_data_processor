BASE_PATH = "/home/jtordai/projects/"
BASE_DATA_PATH = BASE_PATH + "input_data/"
BASE_SHAPEFILE_PATH = BASE_DATA_PATH + "metadata/shapefiles/"
MUNICIPALITY_SHAPEFILE = f"{BASE_SHAPEFILE_PATH}STATISTIK_AUSTRIA_GEM_20230101.shp"

HISTORICAL_DATA_PATH = BASE_DATA_PATH + "climate_data/netcdf/historical/"

ANALYSIS_START_YEAR = 1961
ANALYSIS_END_YEAR = 2021
ENSEMBLE_START_YEAR = 1970
ENSEMBLE_END_YEAR = 2100

STATISTICS = [
    "minimum",
    "lowerPercentile",
    "median",
    "mean",
    "upperPercentile",
    "maximum",
]

STATISTIC_PERIODS_OEKS = [
    ["1971", "2000"],
    ["1981", "2010"],
    ["1991", "2020"],
    ["2021", "2050"],
    ["2036", "2065"],
    ["2041", "2070"],
    ["2071", "2100"],
]

STATISTIC_PERIODS_HISTORICAL = [
    ["1971", "2000"],
    ["1981", "2010"],
    ["1991", "2020"],
]
