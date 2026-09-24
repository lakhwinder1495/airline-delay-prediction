import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
)

from preprocessing import load_and_prepare_data


MODEL_PATH = "models/airline_delay_model.joblib"


def build_model():
    categorical_features = [
        "OP_UNIQUE_CARRIER",
        "ORIGIN_AIRPORT_ID",
        "DEST_AIRPORT_ID",
    ]

    numerical_features = [
        "YEAR",
        "MONTH",
        "DAY_OF_MONTH",
        "DAY_OF_WEEK",
        "OP_CARRIER_FL_NUM",
        "CRS_DEP_TIME",
        "CRS_ARR_TIME",
        "CRS_ELAPSED_TIME",
        "DISTANCE",
        "DEP_HOUR",
        "DEP_MINUTE",
        "ARR_HOUR",
        "DAY_OF_YEAR",
    ]

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    numerical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_pipeline, categorical_features),
            ("numerical", numerical_pipeline, numerical_features),
        ]
    )

    classifier = HistGradientBoostingClassifier(
        max_iter=150,
        learning_rate=0.08,
        max_leaf_nodes=31,
        random_state=42,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def main():
    print("Preparing training data...")

    X, y = load_and_prepare_data()

    # Stratification keeps approximately the same delayed/not-delayed
    # ratio in both training and testing sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"\nTraining rows: {len(X_train):,}")
    print(f"Testing rows:  {len(X_test):,}")

    model = build_model()

    print("\nTraining model...")
    model.fit(X_train, y_train)

    print("Training completed.")

    print("\nEvaluating model...")

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    print("\n==============================")
    print("MODEL PERFORMANCE")
    print("==============================")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()