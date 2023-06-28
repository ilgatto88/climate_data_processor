import geopandas as gpd


def load_shapefile(path: str, encoding: str = "utf-8") -> gpd.GeoDataFrame:
    """Loads a shapefile and returns it as a GeoDataFrame."""
    return gpd.read_file(path, encoding=encoding)


def filter_geodataframe_by_ids(
    dataframe: gpd.GeoDataFrame, values: list[str], column_name: str = "g_id"
) -> gpd.GeoDataFrame:
    """
    Filters a GeoDataFrame based on the values in a specific column
    and returns the filtered GeoDataFrame.
    """
    return dataframe.loc[dataframe[column_name].isin(values)]  # type: ignore
