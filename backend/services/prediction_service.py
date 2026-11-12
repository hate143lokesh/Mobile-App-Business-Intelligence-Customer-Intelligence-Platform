
import joblib
import pandas as pd
import shap
from pathlib import Path

# ==================================================
# 1. LOAD MODEL AND PREPROCESSOR
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "NEXORA_RF_Explainable_Model.pkl"
)

try:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    artifact = joblib.load(MODEL_PATH)

    model = artifact["model"]
    preprocessor = artifact["preprocessor"]
    feature_names = artifact["feature_names"]

    print("Model loaded successfully!")

except Exception as e:
    raise RuntimeError(
        f"Failed to load model: {str(e)}"
    ) from e


# ==================================================
# 2. INITIALIZE SHAP EXPLAINER
# ==================================================

try:
    explainer = shap.TreeExplainer(model)
    print("SHAP explainer initialized successfully!")

except Exception as e:
    raise RuntimeError(
        f"Failed to initialize SHAP: {str(e)}"
    ) from e


# ==================================================
# 3. INPUT VALIDATION
# ==================================================

def validate_input(input_data):

    if not isinstance(input_data, dict):
        raise ValueError("Input must be a dictionary.")

    missing_features = [
        feature
        for feature in feature_names
        if feature not in input_data
    ]

    extra_features = [
        feature
        for feature in input_data
        if feature not in feature_names
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    if extra_features:
        raise ValueError(
            f"Unexpected features: {extra_features}"
        )

    return True


# ==================================================
# 4. PURCHASE PREDICTION
# ==================================================

def predict_purchase(input_data):

    try:
        validate_input(input_data)

        input_df = pd.DataFrame(
            [input_data],
            columns=feature_names
        )

        transformed_data = preprocessor.transform(
            input_df
        )

        prediction = model.predict(
            transformed_data
        )[0]

        probabilities = model.predict_proba(
            transformed_data
        )[0]

        return {
            "prediction": int(prediction),

            "prediction_label": (
                "Purchase"
                if prediction == 1
                else "No Purchase"
            ),

            "purchase_probability": float(
                probabilities[1]
            ),

            "no_purchase_probability": float(
                probabilities[0]
            )
        }

    except (ValueError, TypeError):
        raise

    except Exception as e:
        raise RuntimeError(
            f"Prediction failed: {str(e)}"
        ) from e


# ==================================================
# 5. SHAP EXPLANATION
# ==================================================

def explain_prediction(input_data):

    try:
        validate_input(input_data)

        input_df = pd.DataFrame(
            [input_data],
            columns=feature_names
        )

        transformed_data = preprocessor.transform(
            input_df
        )

        shap_values = explainer.shap_values(
            transformed_data
        )

        # Binary classification: select purchase class
        if isinstance(shap_values, list):
            purchase_shap_values = shap_values[1][0]

        elif len(shap_values.shape) == 3:
            purchase_shap_values = shap_values[0, :, 1]

        else:
            purchase_shap_values = shap_values[0]

        transformed_feature_names = (
            preprocessor.get_feature_names_out()
        )

        explanation_df = pd.DataFrame({
            "feature": transformed_feature_names,
            "shap_value": purchase_shap_values
        })

        explanation_df["impact"] = (
            explanation_df["shap_value"].apply(
                lambda value:
                "Positive" if value > 0
                else "Negative"
            )
        )

        explanation_df = explanation_df.sort_values(
            by="shap_value",
            key=abs,
            ascending=False
        )

        top_features = (
            explanation_df.head(10)
            .to_dict(orient="records")
        )

        return {
            "explanation_method": "SHAP",
            "explained_class": "Purchase",
            "top_features": top_features
        }

    except Exception as e:
        raise RuntimeError(
            f"SHAP explanation failed: {str(e)}"
        ) from e
