"""
04_image_classification.py
LISS-3 Dehradun LULC Classification — Stage 4

Extracted from notebook cells 52-53. Applies the trained final_model to
the full B2/B3/B4/B5 Dehradun raster stack, block-by-block, producing
the classified land-cover raster (classes 1-5, uint8, nodata=0).
"""

import os
import numpy as np
import rasterio

from importlib import import_module
dp = import_module("01_data_preparation")

BASE = dp.BASE


def check_bands(band_paths):
    print("DEHRADUN LISS-3 RASTER CHECK")
    for band_name, path in band_paths.items():
        with rasterio.open(path) as src:
            print(f"\n{band_name}")
            print("CRS:", src.crs)
            print("Width:", src.width, "Height:", src.height)
            print("Resolution:", src.res)
            print("Data type:", src.dtypes[0])
            print("NoData:", src.nodata)
            print("Bounds:", src.bounds)


def classify_image(final_model, band_paths, base=BASE):
    classification_path = os.path.join(
        base, "LISS3_Dehradun_LandCover_Classification.tif"
    )

    src_b2 = rasterio.open(band_paths["B2"])
    src_b3 = rasterio.open(band_paths["B3"])
    src_b4 = rasterio.open(band_paths["B4"])
    src_b5 = rasterio.open(band_paths["B5"])

    profile = src_b2.profile.copy()
    profile.update(dtype=rasterio.uint8, count=1, nodata=0, compress="lzw")

    with rasterio.open(classification_path, "w", **profile) as dst:
        for block_index, window in src_b2.block_windows(1):
            b2 = src_b2.read(1, window=window)
            b3 = src_b3.read(1, window=window)
            b4 = src_b4.read(1, window=window)
            b5 = src_b5.read(1, window=window)

            pixels = np.column_stack([b2.ravel(), b3.ravel(), b4.ravel(), b5.ravel()])
            valid = np.all(np.isfinite(pixels), axis=1)

            predictions = np.zeros(pixels.shape[0], dtype=np.uint8)
            if np.any(valid):
                predictions[valid] = final_model.predict(pixels[valid]).astype(np.uint8)

            predictions = predictions.reshape(b2.shape)
            dst.write(predictions, 1, window=window)
            print(f"Processed block: {block_index}")

    src_b2.close()
    src_b3.close()
    src_b4.close()
    src_b5.close()

    print("\nCLASSIFICATION COMPLETE")
    print("Output:", classification_path)
    return classification_path


if __name__ == "__main__":
    band_paths = dp.get_processed_band_paths()
    check_bands(band_paths)

    # final_model must be trained via 03_model_training.build_final_model()
    # + train_final_model() before calling classify_image().
    mt = import_module("03_model_training")
    te = import_module("02_training_data_extraction")
    import geopandas as gpd

    final_training = gpd.read_file(te.FINAL_GPKG_PATH, layer="training_samples")
    X = final_training[["B2", "B3", "B4", "B5"]]
    y = final_training["class"]

    model = mt.build_final_model()
    model = mt.train_final_model(model, X, y)

    classify_image(model, band_paths)
