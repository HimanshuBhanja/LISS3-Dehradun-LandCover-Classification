"""
01_data_preparation.py
LISS-3 Dehradun LULC Classification — Stage 1

Extracted from LISS3_Dehradun_LULC_Classification.ipynb (cells 2-9, 12).
Reprojects scene_050 -> EPSG:32644, mosaics scene_049 + scene_050 per band,
clips mosaic to Dehradun boundary. No methodology change from notebook.
"""

import os
import glob
import rasterio
import geopandas as gpd
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.merge import merge
from rasterio.mask import mask

BASE = "/content/drive/MyDrive/Python Project/LISS3_Dehradun"
BANDS = ["BAND2", "BAND3", "BAND4", "BAND5"]
TARGET_CRS = "EPSG:32644"
MOSAIC_RES = (24, 24)


def reproject_scene_050(base=BASE, target_crs=TARGET_CRS):
    scene_050 = os.path.join(base, "scene_050")
    reprojected_dir = os.path.join(base, "reprojected_32644")
    os.makedirs(reprojected_dir, exist_ok=True)

    for band in BANDS:
        input_path = os.path.join(scene_050, f"{band}.tif")
        output_path = os.path.join(reprojected_dir, f"{band}_scene050_32644.tif")

        with rasterio.open(input_path) as src:
            transform, width, height = calculate_default_transform(
                src.crs, target_crs, src.width, src.height, *src.bounds
            )
            profile = src.profile.copy()
            profile.update({
                "crs": target_crs,
                "transform": transform,
                "width": width,
                "height": height
            })
            with rasterio.open(output_path, "w", **profile) as dst:
                reproject(
                    source=rasterio.band(src, 1),
                    destination=rasterio.band(dst, 1),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.nearest
                )
        print(f"Done: {band} -> {output_path}")

    return reprojected_dir


def mosaic_and_clip(base=BASE, target_crs=TARGET_CRS):
    scene_049 = os.path.join(base, "scene_049")
    reprojected_dir = os.path.join(base, "reprojected_32644")
    shapefile = os.path.join(base, "Dehradun_boundary", "Dehradun.shp")
    output_dir = os.path.join(base, "processed")
    os.makedirs(output_dir, exist_ok=True)

    gdf = gpd.read_file(shapefile)
    print("Original boundary CRS:", gdf.crs)
    gdf = gdf.to_crs(target_crs)
    print("Boundary CRS for processing:", gdf.crs)

    for band in BANDS:
        print(f"\nPROCESSING {band}")

        file_049 = os.path.join(scene_049, f"{band}.tif")
        file_050 = os.path.join(reprojected_dir, f"{band}_scene050_32644.tif")

        src1 = rasterio.open(file_049)
        src2 = rasterio.open(file_050)

        mosaic, mosaic_transform = merge([src1, src2], res=MOSAIC_RES)
        print("Mosaic shape:", mosaic.shape)

        mosaic_meta = src1.meta.copy()
        mosaic_meta.update({
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": mosaic_transform,
            "crs": target_crs,
            "count": 1,
            "tiled": True,
            "blockxsize": 256,
            "blockysize": 256,
            "compress": "deflate"
        })

        mosaic_path = os.path.join(output_dir, f"{band}_mosaic_32644.tif")
        with rasterio.open(mosaic_path, "w", **mosaic_meta) as dst:
            dst.write(mosaic)
        print("Mosaic saved:", mosaic_path)

        src1.close()
        src2.close()

        with rasterio.open(mosaic_path) as src:
            clipped, clipped_transform = mask(src, gdf.geometry, crop=True)
            clipped_meta = src.meta.copy()
            clipped_meta.update({
                "driver": "GTiff",
                "height": clipped.shape[1],
                "width": clipped.shape[2],
                "transform": clipped_transform,
                "crs": target_crs,
                "count": 1,
                "tiled": True,
                "blockxsize": 256,
                "blockysize": 256,
                "compress": "deflate"
            })
            output_path = os.path.join(output_dir, f"{band}_Dehradun.tif")
            with rasterio.open(output_path, "w", **clipped_meta) as dst:
                dst.write(clipped)
        print("Clipped successfully:", output_path)

    print("\nFINAL DEHRADUN LISS-3 DATASETS")
    for f in sorted(glob.glob(os.path.join(output_dir, "*_Dehradun.tif"))):
        print(f)

    return output_dir


def get_processed_band_paths(base=BASE):
    """Returns dict of final clipped per-band raster paths (B2-B5)."""
    processed = os.path.join(base, "processed")
    return {
        "B2": os.path.join(processed, "BAND2_Dehradun.tif"),
        "B3": os.path.join(processed, "BAND3_Dehradun.tif"),
        "B4": os.path.join(processed, "BAND4_Dehradun.tif"),
        "B5": os.path.join(processed, "BAND5_Dehradun.tif"),
    }


if __name__ == "__main__":
    reproject_scene_050()
    mosaic_and_clip()
    print(get_processed_band_paths())
