from pydantic import BaseModel, Field

class LoanApplication(BaseModel):
    application_month: str  # Optional if not used in training
    customer_age: int = Field(..., gt=17)
    employment_type: str
    monthly_income: float
    credit_score: int
    time_in_job_months: int
    loan_amount: float
    loan_term_months: int
    loan_type: str
    loan_purpose: str
    existing_loan_count: int
    existing_emi_total: float
    dti_ratio: float
    prev_defaults_count: int
