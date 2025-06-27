from fastapi import APIRouter
from app.schemas import LoanApplication
from app.model_loader import get_model
from app.fetch_macro import get_macro_indicators
import pandas as pd

router = APIRouter()

@router.post("/predict")
def predict_loan(data: LoanApplication):
    input_df = pd.DataFrame([data.dict()])

    if "application_month" in input_df.columns:
        input_df.drop(columns=["application_month"], inplace=True)

    encode_maps = {
        "employment_type": {"Salaried": 0, "Self-Employed": 1},
        "loan_type": {
            "Personal": 0,
            "Home": 1,
            "Auto": 2,
            "Business": 3
        },
        "loan_purpose": {
            "Education": 0,
            "Business": 1,
            "Medical Emergency": 2,
            "Business Expansion": 3,
            "Home Improvement": 4,
            "Vehicle Purchase": 5,
            "Wedding": 6
        }
    }

    for col, mapping in encode_maps.items():
        if col in input_df.columns:
            input_df[col] = input_df[col].map(mapping)

    use_macro = (
        (input_df["loan_amount"].iloc[0] >= 500000) or
        (input_df["loan_type"].iloc[0] in [1, 3]) or
        (input_df["loan_purpose"].iloc[0] in [3, 4])
    )

    if use_macro:
        macro_data = get_macro_indicators()
        for key, value in macro_data.items():
            input_df[key] = value

    # ✅ Final Fix: Ensure correct column order
    macro_feature_order = [
        "customer_age", "employment_type", "monthly_income", "credit_score", "time_in_job_months",
        "loan_amount", "loan_term_months", "loan_type", "loan_purpose",
        "existing_loan_count", "existing_emi_total", "dti_ratio", "prev_defaults_count",
        "employment_rate", "interest_rate", "inflation_rate", "gdp_growth_rate"
    ]

    basic_feature_order = [
        "customer_age", "employment_type", "monthly_income", "credit_score", "time_in_job_months",
        "loan_amount", "loan_term_months", "loan_type", "loan_purpose",
        "existing_loan_count", "existing_emi_total", "dti_ratio", "prev_defaults_count"
    ]

    input_df = input_df[macro_feature_order if use_macro else basic_feature_order]

    model = get_model(use_macro=use_macro)
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][int(prediction)]

    return {
        "loan_approved": bool(int(prediction)),
        "confidence": round(float(probability), 3),
        "model_used": "macro" if use_macro else "basic"
    }
