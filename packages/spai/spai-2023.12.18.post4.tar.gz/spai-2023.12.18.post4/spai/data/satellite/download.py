from .sentinelhub import SHS2L2ADownloader, SHS2L1CDownloader, SHS1Downloader, SHDEM30Downloader
from .utils import create_aoi_geodataframe
import shutil
import os
import geopandas as gpd
from .explore import explore_satellite_images


def download_satellite_image(storage, aoi, date=None, sensor="S2L2A", **kwargs):
    if date is None:
        options = explore_satellite_images(aoi, sensor=sensor, **kwargs)
        if len(options) == 0:
            raise ValueError("No images found")
        date = options[0]["date"].split("T")[0]
    gdf = create_aoi_geodataframe(aoi)
    if isinstance(gdf, gpd.GeoDataFrame):
        download_dir = "/tmp/sentinelhub"
        if sensor == "S2L2A":
            downloader = SHS2L2ADownloader(download_dir)
        elif sensor == "S2L1C":
            downloader = SHS2L1CDownloader(download_dir)
        elif sensor == "S1":
            downloader = SHS1Downloader(download_dir)
        else:
            raise Exception(f"sensor {sensor} not supported")
        if isinstance(date, str):
            dst_path = downloader.download(gdf, date)
            dst_path = storage.create(dst_path, name=f"{sensor}_{date}.tif")
            shutil.rmtree(download_dir)
            return dst_path
        # elif isinstance(date,list):
        #     dst_paths = []
        #     for d in date:
        #         dst_path = downloader.download(gdf, d)
        #         dst_path = storage.create(dst_path, name=f"{sensor}_{d}.tif")
        #         dst_paths.append(dst_path)
        #     shutil.rmtree(download_dir)
        #     return dst_paths
        else:
            raise Exception(f"Date type {type(date)} not supported")
    else:
        return gdf


def download_dem(storage, aoi, **kwargs):
    gdf = create_aoi_geodataframe(aoi)
    if isinstance(gdf, gpd.GeoDataFrame):
        download_dir = "/tmp/sentinelhub"
        downloader = SHDEM30Downloader()
        dst_path = downloader.download(gdf, date=None)
        dst_path = storage.create(dst_path, name="DEM.tif")
        shutil.rmtree(download_dir) if os.path.exists(download_dir) else None
        return dst_path
    else:
        return gdf
