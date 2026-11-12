
from fastapi import APIRouter, HTTPException

from backend.schemas.prediction import (
    PredictionInput,
    PredictionOutput
)

from backend.services.prediction_service import (
    predict_purchase,
    explain_prediction
)

router = APIRouter()


# ==================================================
# 1. PURCHASE PREDICTION API
# ==================================================

@router.post(
    "/predict",
    response_model=PredictionOutput,
    summary="Predict Customer Purchase",
    description="""
    Predict whether a customer will purchase a product
    using the trained Random Forest model.
    """
)
def predict(input_data: PredictionInput):

    try:
        result = predict_purchase(
            input_data.model_dump()
        )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected prediction error."
        )


# ==================================================
# 2. SHAP EXPLANATION API
# ==================================================

@router.post(
    "/explain",
    summary="Explain Customer Purchase Prediction",
    description="""
    Explains the factors influencing a customer's
    purchase prediction using SHAP.
    """
)
def explain(input_data: PredictionInput):

    try:
        result = explain_prediction(
            input_data.model_dump()
        )

        return {
            "success": True,
            "message": "SHAP explanation generated successfully",
            "explanation": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected explanation error."
        )
