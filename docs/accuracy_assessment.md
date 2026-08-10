# Accuracy Assessment

## Model

The final classification model was Polynomial Logistic Regression.

Configuration:

- Polynomial degree: 2
- C: 100
- Solver: lbfgs
- Class weight: None
- Maximum iterations: 5000

## Training Dataset

Total samples: **516**

Features:

- B2
- B3
- B4
- B5

Classes:

1. Forest
2. Agriculture
3. Water
4. Urban
5. Barren

## Cross-Validation

A stratified 10-fold cross-validation procedure was used.

| Metric | Result |
|---|---:|
| Mean CV Accuracy | 61.82% |
| Standard Deviation | 4.72% |
| Minimum Fold Accuracy | 51.92% |
| Maximum Fold Accuracy | 69.23% |

## Classification Report

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Forest | 0.76 | 0.84 | 0.80 |
| Agriculture | 0.50 | 0.51 | 0.50 |
| Water | 0.79 | 0.57 | 0.66 |
| Urban | 0.55 | 0.72 | 0.62 |
| Barren | 0.53 | 0.44 | 0.48 |

## Confusion Matrix

The confusion matrix is provided in:

`../results/confusion_matrix.png`

## Interpretation

Forest showed the strongest classification performance, with
an F1-score of 0.80.

Water achieved high precision but had moderate recall.

Agriculture and Barren showed greater spectral confusion with
other land-cover classes.

The overall cross-validated accuracy of 61.82% indicates
moderate classification performance using only the four
LISS-3 spectral bands.
