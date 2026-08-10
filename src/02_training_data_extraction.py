"""
02_training_data_extraction.py
LISS-3 Dehradun LULC Classification — Stage 2

Extracted from notebook cells 32-39, 44-48 (final working logic only;
exploratory spectral summaries / early 100-point dataset from cells 14-21
remain in the notebook and are not duplicated here).

Loads the 516-point training_points.gpkg, extracts B2/B4/B5/B3 spectral
values, runs QC (missing/zero/outlier checks), corrects the one verified
mislabeled point (index 179 -> class 5), and writes the final training
GeoPackage used for model training.
"""

import os
import rasterio
import geopandas as gpd
import pandas as pd

from importlib import import_module
dp = import_module("01_data_preparation")

BASE = dp.BASE
NEW_TRAINING_PATH = "/content/drive/MyDrive/Python Project/training_points.gpkg"
FINAL_GPKG_PATH = os.path.join(BASE, "LISS3_Dehradun_Training_Data_516.gpkg")

CLASS_NAMES = {1: "Forest", 2: "Agriculture", 3: "Water", 4: "Urban", 5: "Barren"}


def load_training_points(path=NEW_TRAINING_PATH):
    training_new = gpd.read_file(path)
    print("Number of points:", len(training_new))
    print("Class distribution:")
    print(training_new["classes"].value_counts().sort_index())
    return training_new


def extract_spectral_values(training_new, raster_paths):
    coords = [(geom.x, geom.y) for geom in training_new.geometry]

    samples_new = pd.DataFrame({
        "class": training_new["classes"].astype(int).values
    })

    for band_name, raster_path in raster_paths.items():
        with rasterio.open(raster_path) as src:
            values = [value[0] for value in src.sample(coords)]
            samples_new[band_name] = values

    samples_new = samples_new[["B2", "B3", "B4", "B5", "class"]]
    print("Dataset shape:", samples_new.shape)
    return samples_new


def quality_checks(samples_new):
    print("Missing values:")
    print(samples_new.isna().sum())
    print("\nZero values:")
    print((samples_new[["B2", "B3", "B4", "B5"]] == 0).sum())
    print("\nSpectral statistics:")
    print(samples_new[["B2", "B3", "B4", "B5"]].describe())


def apply_verified_correction(training_new, samples_new):
    """Applies the single verified mislabel correction identified during
    outlier review (point index 179, corrected Forest -> Barren, class 5)."""
    training_new.loc[179, "classes"] = 5
    samples_new.loc[179, "class"] = 5
    print("Corrected point 179.")
    print("Updated class distribution:")
    print(samples_new["class"].value_counts().sort_index())
    return training_new, samples_new


def save_final_training_dataset(training_new, samples_new, gpkg_path=FINAL_GPKG_PATH):
    final_training = training_new.copy()
    final_training["B2"] = samples_new["B2"].values
    final_training["B3"] = samples_new["B3"].values
    final_training["B4"] = samples_new["B4"].values
    final_training["B5"] = samples_new["B5"].values
    final_training["class"] = samples_new["class"].astype(int)

    final_training = final_training[["B2", "B3", "B4", "B5", "class", "geometry"]]

    final_training.to_file(gpkg_path, layer="training_samples", driver="GPKG")

    print("Final training GeoPackage saved:", gpkg_path)
    print("Shape:", final_training.shape)
    print("Class distribution:")
    print(final_training["class"].value_counts().sort_index())

    return final_training


if __name__ == "__main__":
    raster_paths = dp.get_processed_band_paths()
    training_new = load_training_points()
    samples_new = extract_spectral_values(training_new, raster_paths)
    quality_checks(samples_new)
    training_new, samples_new = apply_verified_correction(training_new, samples_new)
    final_training = save_final_training_dataset(training_new, samples_new)
