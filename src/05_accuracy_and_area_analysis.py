"""
05_accuracy_and_area_analysis.py
LISS-3 Dehradun LULC Classification — Stage 5

Extracted from notebook cells 42, 55, 56, 58.
Reports out-of-fold cross-validated accuracy of the final model, then
computes land-cover area statistics (pixel counts, ha, km2, %) from the
classified raster, plus a boundary-consistency check.
"""

import numpy as np
import pandas as pd
import rasterio
import geopandas as gpd
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

CLASS_NAMES = {1: "Forest", 2: "Agriculture", 3: "Water", 4: "Urban", 5: "Barren"}
CLASS_LABELS = [1, 2, 3, 4, 5]
CLASS_NAME_LIST = ["Forest", "Agriculture", "Water", "Urban", "Barren"]


def cv_accuracy_report(final_model, X, y, cv_splits=10, random_state=42):
    cv10 = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=random_state)
    y_pred_cv = cross_val_predict(final_model, X, y, cv=cv10, method="predict")

    print("Overall CV Accuracy:", f"{accuracy_score(y, y_pred_cv) * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(
        y, y_pred_cv, labels=CLASS_LABELS,
        target_names=CLASS_NAME_LIST, zero_division=0
    ))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y, y_pred_cv, labels=CLASS_LABELS))
    return y_pred_cv


def raster_area_summary(classification_path):
    with rasterio.open(classification_path) as src:
        classified = src.read(1)
        pixel_area_m2 = abs(src.res[0] * src.res[1])
        values, counts = np.unique(classified, return_counts=True)

        results = []
        for value, count in zip(values, counts):
            if value == 0:
                continue
            area_m2 = count * pixel_area_m2
            results.append({
                "Class": int(value),
                "Land Cover": CLASS_NAMES.get(int(value), "Unknown"),
                "Pixels": int(count),
                "Area_m2": area_m2,
                "Area_ha": area_m2 / 10000,
                "Area_km2": area_m2 / 1_000_000
            })

    area_df = pd.DataFrame(results)
    print("DEHRADUN LISS-3 LAND COVER AREA")
    print(area_df.to_string(index=False, formatters={
        "Area_m2": "{:,.2f}".format,
        "Area_ha": "{:,.2f}".format,
        "Area_km2": "{:,.4f}".format
    }))
    print("\nTotal classified area:", f"{area_df['Area_km2'].sum():.4f} km2")
    return area_df


def boundary_consistency_check(classification_path, boundary_path):
    boundary = gpd.read_file(boundary_path)
    print("Boundary area:",
          boundary.to_crs("EPSG:32644").geometry.area.sum() / 1e6, "km2")

    with rasterio.open(classification_path) as src:
        print("Raster area:",
              src.width * src.height * abs(src.res[0] * src.res[1]) / 1e6, "km2")
        classified = src.read(1)
        print("Unique values:", np.unique(classified, return_counts=True))


def clipped_mask_verification(clipped_path):
    with rasterio.open(clipped_path) as src:
        classified = src.read(1)
        values, counts = np.unique(classified, return_counts=True)

        print("MASK VERIFICATION")
        for value, count in zip(values, counts):
            name = "NoData / Outside Boundary" if value == 0 else CLASS_NAMES.get(int(value), "Unknown")
            print(f"Value {value}: {name} = {count:,} pixels")

        pixel_area_m2 = abs(src.res[0] * src.res[1])
        valid_mask = classified != 0
        valid_pixels = np.sum(valid_mask)

        print("\nValid pixels:", f"{valid_pixels:,}")
        print("Valid area:", f"{valid_pixels * pixel_area_m2 / 1e6:.4f} km2")

        results = []
        for class_id in range(1, 6):
            pixel_count = np.sum(classified == class_id)
            area_m2 = pixel_count * pixel_area_m2
            results.append({
                "Class": class_id,
                "Land Cover": CLASS_NAMES[class_id],
                "Pixels": int(pixel_count),
                "Area_ha": area_m2 / 10000,
                "Area_km2": area_m2 / 1e6,
                "Percentage": pixel_count / valid_pixels * 100
            })

    area_df = pd.DataFrame(results)
    print("\nFINAL DEHRADUN LAND COVER STATISTICS")
    print(area_df.to_string(index=False, formatters={
        "Area_ha": "{:,.2f}".format,
        "Area_km2": "{:,.4f}".format,
        "Percentage": "{:.2f}%".format
    }))
    print("\nTotal:", f"{area_df['Area_km2'].sum():,.4f} km2",
          f"{area_df['Percentage'].sum():.2f}%")
    return area_df


if __name__ == "__main__":
    from importlib import import_module
    dp = import_module("01_data_preparation")
    classification_path = f"{dp.BASE}/LISS3_Dehradun_LandCover_Classification.tif"
    boundary_path = f"{dp.BASE}/Dehradun_boundary/Dehradun.shp"
    clipped_path = f"{dp.BASE}/LISS3_Dehradun_LandCover_Classification_Clipped.tif"

    raster_area_summary(classification_path)
    boundary_consistency_check(classification_path, boundary_path)
    # Run 06_visualization_and_export.py first to produce clipped_path
    clipped_mask_verification(clipped_path)
