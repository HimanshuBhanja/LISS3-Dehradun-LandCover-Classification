# Methodology

## 1. Study Area

The study focuses on Dehradun district, Uttarakhand, India.

The Dehradun boundary was used to mask the final land-cover
classification.

## 2. Satellite Data

Resourcesat-2 LISS-3 multispectral imagery was used.

The following LISS-3 bands were used:

- B2
- B3
- B4
- B5

Spatial resolution: 24 m

Final processing CRS: EPSG:32644

## 3. Image Preprocessing

Two LISS-3 scenes were processed.

Scene 049 was available in EPSG:32644, while Scene 050 was
reprojected from EPSG:32643 to EPSG:32644.

The corresponding bands were mosaicked and prepared for
Dehradun-level analysis.

## 4. Training Data

Training samples were collected for five land-cover classes:

| Class | Land Cover |
|---|---|
| 1 | Forest |
| 2 | Agriculture |
| 3 | Water |
| 4 | Urban |
| 5 | Barren |

A total of 516 training samples were used.

Spectral features consisted of:

- B2
- B3
- B4
- B5

## 5. Classification Algorithm

Polynomial Logistic Regression was used.

The model consisted of:

- Polynomial degree: 2
- StandardScaler
- Logistic Regression
- C = 100
- Solver = lbfgs
- Maximum iterations = 5000

## 6. Accuracy Assessment

Stratified 10-fold cross-validation was used.

The mean cross-validation accuracy was:

**61.82%**

Standard deviation:

**4.72%**

## 7. Full Image Classification

The trained model was applied to the complete LISS-3 imagery
using B2, B3, B4 and B5.

Classification was performed using memory-efficient raster
block processing.

## 8. Boundary Masking

The classified raster was masked using the Dehradun boundary.

Pixels outside the boundary were assigned NoData.

The final valid classified area was approximately:

**3,071.00 km²**

## 9. Area Calculation

Each LISS-3 pixel represents:

24 m × 24 m = 576 m²

Class areas were calculated in square metres, hectares and
square kilometres.

The percentage of each class was calculated relative to the
total valid Dehradun classified area.
