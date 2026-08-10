# LISS-3 Dehradun Land Cover Classification

## Project Data Repository

This folder contains the satellite imagery, processed datasets, training data, and final land-cover classification outputs used for the **LISS-3 based Land Cover Classification of Dehradun** project.

## Google Drive Data

The complete project data and large files are provided through Google Drive:

**[Open Google Drive Folder](https://drive.google.com/drive/folders/1XMiX_miH8dasSoXl4_NkXD9PuAmQxkbD?usp=sharing)**

The project uses LISS-3 multispectral imagery and machine-learning classification to map five land-cover classes:

1. Forest
2. Agriculture
3. Water
4. Urban
5. Barren

---

## Folder Structure

```text
LISS3_Dehradun/
│
├── processed/
│   └── Processed LISS-3 datasets
│
├── reprojected_32644/
│   └── Reprojected datasets in EPSG:32644
│
├── scene_049/
│   └── LISS-3 Scene 049 data
│
├── scene_050/
│   └── LISS-3 Scene 050 data
│
├── LISS3_Dehradun_LandCover_Classification.tif
│   └── Final classified land-cover raster
│
├── LISS3_Dehradun_Training_Data.gpkg
│   └── Training samples in GeoPackage format
│
└── training_points.gpkg
    └── Training point layer used for sample preparation
```

---

## Main Files

### Final Classification Raster

`LISS3_Dehradun_LandCover_Classification.tif`

This is the final LISS-3 land-cover classification raster for the Dehradun study area.

Class codes:

| Class | Land Cover |
|------:|------------|
| 1 | Forest |
| 2 | Agriculture |
| 3 | Water |
| 4 | Urban |
| 5 | Barren |

### Training Data

`LISS3_Dehradun_Training_Data.gpkg`

Contains the spatial training samples used for machine-learning classification.

### Training Points

`training_points.gpkg`

Contains the training point geometries and class labels used during training sample preparation.

---

## Satellite Data

The original and intermediate LISS-3 data are organized into:

- `scene_049/`
- `scene_050/`
- `reprojected_32644/`
- `processed/`

These datasets are kept on Google Drive because satellite imagery and intermediate raster datasets can be large and are not included directly in the GitHub repository.

---

## Coordinate Reference System

The primary processing CRS used for the project is:

```text
EPSG:32644
WGS 84 / UTM Zone 44N
```

---

## Machine Learning

The classification workflow uses **Polynomial Logistic Regression** with LISS-3 spectral bands:

```text
B2
B3
B4
B5
```

The final model was trained using the project training dataset.

---

## GitHub Repository

The source code, notebook, documentation, training data, and selected final outputs are available in the GitHub repository:

**[LISS3-Dehradun-LandCover-Classification](https://github.com/HimanshuBhanja/LISS3-Dehradun-LandCover-Classification)**

---

## Data Access

For large satellite datasets and files not stored in GitHub, use the Google Drive folder linked above.

Please download the required files while preserving the folder structure where possible.

---

## Author

**Himanshu Bhanja**

M.Sc. Agriculture Analytics

---

## Note

The Google Drive folder should be set to:

**Anyone with the link → Viewer**

so that users can access the data without requesting permission.
