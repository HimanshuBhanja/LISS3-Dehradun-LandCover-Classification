# LISS3-Dehradun-LandCover-Classification

LULC classification of Dehradun from LISS-3 imagery (scene_049 +
scene_050) using Polynomial Logistic Regression (degree=2, C=100).

## Entry point

[`notebooks/LISS3_Dehradun_LULC_Classification.ipynb`](notebooks/LISS3_Dehradun_LULC_Classification.ipynb)
— complete, unmodified end-to-end workflow: data prep, CRS handling,
mosaicking, training extraction, model experimentation (plain vs.
polynomial logistic regression, C-tuning, 10-fold CV), final model,
classification, masking, area stats. Read this first.

## Modular scripts (`src/`)

Clean modular extraction of the notebook's FINAL working logic only
(exploratory/model-comparison code stays in the notebook).

| Script | Purpose |
|---|---|
| `01_data_preparation.py` | Reproject scene_050, mosaic scene_049+050, clip to boundary |
| `02_training_data_extraction.py` | Extract B2-B5 at 516 points, QC, correct verified mislabel, save training gpkg |
| `03_model_training.py` | Build + CV + fit final Polynomial Logistic Regression |
| `04_image_classification.py` | Block-wise full-raster classification |
| `05_accuracy_and_area_analysis.py` | CV accuracy, area stats, boundary check, visualization, clipped export |

Run order: `01 -> 02 -> 03 -> 04 -> 05`.

## Repo layout

- `data/raw/` — input LISS-3 scenes + boundary zip (gitignored)
- `data/training/` — final 516-pt training GeoPackage
- `data/boundary/` — Dehradun boundary shapefile
- `outputs/` — classification raster, map PNG, area stats CSV
- `docs/` — methodology + accuracy assessment write-ups
- `results/` — confusion matrix + classification report

Class scheme: 1 Forest, 2 Agriculture, 3 Water, 4 Urban, 5 Barren.
CRS: EPSG:32644.
