"""
03_model_training.py
LISS-3 Dehradun LULC Classification — Stage 3

Extracted from notebook cells 49, 51 (final selected model only).
Model-selection experiments — plain multinomial logistic regression,
C-value sweep, and the standard vs. polynomial CV comparison — remain
in the notebook (cells 22-31, 41-42, 50) and are not reproduced here;
this script trains only the FINAL chosen model.

Final model: Polynomial (degree=2) Logistic Regression
  - PolynomialFeatures(degree=2, include_bias=False)
  - StandardScaler
  - LogisticRegression(C=100, class_weight=None, solver="lbfgs", max_iter=5000)
Selected via 10-fold stratified cross-validation (random_state=42).
"""

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LogisticRegression

CV_SPLITS = 10
RANDOM_STATE = 42
POLY_DEGREE = 2
C_VALUE = 100
MAX_ITER = 5000


def build_final_model():
    return Pipeline([
        ("poly", PolynomialFeatures(degree=POLY_DEGREE, include_bias=False)),
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(
            C=C_VALUE,
            class_weight=None,
            solver="lbfgs",
            max_iter=MAX_ITER
        ))
    ])


def cross_validate(final_model, X, y):
    cv10 = StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(final_model, X, y, cv=cv10, scoring="accuracy")

    print("10-Fold Accuracy:")
    for i, score in enumerate(scores, start=1):
        print(f"Fold {i}: {score * 100:.2f}%")
    print("\nMean CV Accuracy:", f"{scores.mean() * 100:.2f}%")
    print("Standard Deviation:", f"{scores.std() * 100:.2f}%")
    print("Minimum Accuracy:", f"{scores.min() * 100:.2f}%")
    print("Maximum Accuracy:", f"{scores.max() * 100:.2f}%")

    return scores


def train_final_model(final_model, X, y):
    final_model.fit(X, y)
    print("Final Polynomial Logistic Regression trained successfully.")
    print("Training samples:", len(X))
    print("Features:", X.columns.tolist())
    print("Polynomial degree:", POLY_DEGREE, "| C:", C_VALUE, "| Solver: lbfgs")
    return final_model


if __name__ == "__main__":
    from importlib import import_module
    te = import_module("02_training_data_extraction")

    final_training = te.save_final_training_dataset  # reuse existing gpkg if available
    import geopandas as gpd
    final_training = gpd.read_file(te.FINAL_GPKG_PATH, layer="training_samples")

    X = final_training[["B2", "B3", "B4", "B5"]]
    y = final_training["class"]

    model = build_final_model()
    cross_validate(model, X, y)
    train_final_model(model, X, y)
