from dataclasses import dataclass

import geopandas

import config
import geodataframe_tools
from static_geo import VIENNA_GIDS


@dataclass
class MunicipalityDataSettings:
    """Stores settings for 1 dimensional climate data."""

    municipalityId: int
    climateParameter: str
    temporal_resolution: str
    analysis_start_year: int
    analysis_end_year: int
    ensemble_start_year: int
    ensemble_end_year: int
    shape: geopandas.GeoDataFrame

    def create_future_input_file_path(self, scenario: str) -> str:
        """Creates the future input file path string."""
        return (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/{scenario}/"
            f"oeks-{scenario}-{self.climateParameter}-austria-YS.nc"
        )

    def load_geodataframe(self) -> geopandas.GeoDataFrame:
        """Loads the geodataframe for the chosen municipality."""
        id_list = (
            VIENNA_GIDS if self.municipalityId == 90000 else [str(self.municipalityId)]
        )
        return geodataframe_tools.filter_geodataframe_by_ids(self.shape, id_list)
