"""
module that resolve the streets and neighborhoods of Latvia
"""
from abc import ABC, abstractmethod
from enum import Enum
from os import environ
from pathlib import Path
from typing import Dict

import geopandas as gpd  # type: ignore
import pandas as pd  # type: ignore
import pyproj  # type: ignore


class Language(str, Enum):
    EN = "EN"
    LAV = "LAV"


class Resolver(ABC):
    def __init__(self) -> None:
        self._gdf = self.read()
        super().__init__()

    @abstractmethod
    def read(self) -> gpd.GeoDataFrame:
        ...

    @abstractmethod
    def get_translation_dict(self) -> Dict[str, str]:
        ...

    def get_gdf(self, language: Language = Language.LAV):
        match language:
            case language.EN:
                return self._gdf.rename(columns=self.get_translation_dict())
            case Language.LAV | _:
                return self._gdf


class SteetsResolver(Resolver):
    def read(self) -> gpd.GeoDataFrame:
        if filepath := environ.get("STREETS_FILE"):  # type: ignore
            filepath = Path(filepath)  # type: ignore
            print(f"will use external file {filepath}")
        else:
            filepath = Path(__file__).parent / "data/adreses.shp"  # type: ignore
        gdf = gpd.read_file(filepath).to_crs(3059)
        gdf = gdf.apply(
            lambda col: col.map(lambda s: s.lower() if isinstance(s, str) else s)
        )
        gdf["adrese"] = gdf["adrese"].str.replace(" k-", "k-")
        lks92 = pyproj.CRS.from_epsg(3059)
        wgs84 = pyproj.CRS.from_epsg(4326)
        transformer = pyproj.Transformer.from_crs(lks92, wgs84, always_xy=True)

        def convert_coordinates(row):
            x, y = row["X"], row["Y"]
            lon, lat = transformer.transform(x, y)
            return pd.Series({"lat": lat, "lon": lon})

        gdf[["lat", "lon"]] = gdf.apply(convert_coordinates, axis=1)
        return gdf.dropna()

    def get_translation_dict(self) -> Dict[str, str]:
        translation_dict = {
            "Nr": "Number",
            "X": "X",
            "Y": "Y",
            "lat": "lat",
            "lon": "lon",
            "iela": "Street",
            "adrese": "Address",
            "geometry": "Geometry",
        }
        return translation_dict


class NeighborhoodsResolver(Resolver):
    def read(self) -> gpd.GeoDataFrame:
        if filepath := environ.get("NEIGHBORHOODS_FILE"):  # type: ignore
            filepath = Path(filepath)  # type: ignore
            print(f"will use external file {filepath}")
        else:
            filepath = Path(__file__).parent / "data/Apkaimes.shp"  # type: ignore
        gdf = gpd.read_file(filepath)
        gdf = gdf.apply(
            lambda col: col.map(lambda s: s.lower() if isinstance(s, str) else s)
        )
        return gdf.dropna()

    def get_translation_dict(self) -> Dict[str, str]:
        translation_dict = {
            "Code": "Code",
            "Name": "Name",
            "geometry": "geometry",
        }
        return translation_dict


class SteetsAndNeighborhoodsResolver(Resolver):
    def __init__(self) -> None:
        self._streets_resolver = SteetsResolver()
        self._neighborhoods_resolver = NeighborhoodsResolver()
        super().__init__()

    def read(self) -> gpd.GeoDataFrame:
        streets_gdf = self._streets_resolver.get_gdf()
        neighborhoods_gdf = self._neighborhoods_resolver.get_gdf()
        return streets_gdf.sjoin(
            neighborhoods_gdf, how="left", predicate="within"
        ).dropna()

    def get_translation_dict(self) -> Dict[str, str]:
        all_dict: Dict[str, str] = dict()
        all_dict.update(**self._streets_resolver.get_translation_dict())
        all_dict.update(**self._neighborhoods_resolver.get_translation_dict())
        return all_dict
