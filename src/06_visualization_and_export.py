"""
06_visualization_and_export.py
LISS-3 Dehradun LULC Classification — Stage 6

Extracted from notebook cells 29, 43, 57.
Produces spectral-signature and per-class boxplot visualizations, and
clips the final classification raster to the Dehradun boundary for
delivery/export (nodata=0, lzw compression).
"""

import os
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import matplotlib.pyplot as plt

CLASS_NAMES = {1: "Forest", 2: "Agriculture", 3: "Water", 4: "Urban", 5: "Barren"}
BANDS = ["B2", "B3", "B4", "B5"]


def plot_spectral_signatures(samples, class_names=CLASS_NAMES):
    plt.figure(figsize=(10, 6))
    for class_id, name in class_names.items():
        mean_values = samples[samples["class"] == class_id][BANDS].mean()
        plt.plot(BANDS, mean_values, marker="o", label=name)

    plt.xlabel("LISS-3 Spectral Band")
    plt.ylabel("Mean Pixel Value")
    plt.title("Mean LISS-3 Spectral Signatures by Land-Cover Class")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_class_boxplots(samples_new, plot_classes={2: "Agriculture", 4: "Urban", 5: "Barren"}):
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))

    for i, band in enumerate(BANDS):
        data, labels = [], []
        for class_id, class_name in plot_classes.items():
            values = samples_new[samples_new["class"] == class_id][band]
            data.append(values)
            labels.append(class_name)

        axes[i].boxplot(data, tick_labels=labels)
        axes[i].set_title(band)
        axes[i].set_ylabel("LISS-3 pixel value")
        axes[i].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()


def clip_classification_to_boundary(classification_path, boundary_path, output_path):
    boundary = gpd.read_file(boundary_path)

    with rasterio.open(classification_path) as src:
        boundary_raster_crs = boundary.to_crs(src.crs)
        geometries = boundary_raster_crs.geometry.values

        clipped_image, clipped_transform = mask(src, geometries, crop=True, nodata=0)

        clipped_profile = src.profile.copy()
        clipped_profile.update({
            "height": clipped_image.shape[1],
            "width": clipped_image.shape[2],
            "transform": clipped_transform,
            "nodata": 0,
            "compress": "lzw"
        })

        with rasterio.open(output_path, "w", **clipped_profile) as dst:
            dst.write(clipped_image)

    print("CLASSIFIED RASTER CLIPPED TO DEHRADUN")
    print("Output:", output_path)
    return output_path


if __name__ == "__main__":
    from importlib import import_module
    dp = import_module("01_data_preparation")

    classification_path = os.path.join(
        dp.BASE, "LISS3_Dehradun_LandCover_Classification.tif"
    )
    boundary_path = os.path.join(dp.BASE, "Dehradun_boundary", "Dehradun.shp")
    clipped_path = os.path.join(
        dp.BASE, "LISS3_Dehradun_LandCover_Classification_Clipped.tif"
    )

    clip_classification_to_boundary(classification_path, boundary_path, clipped_path)
