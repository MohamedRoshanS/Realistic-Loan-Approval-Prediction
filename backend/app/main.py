from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import predict  # this assumes predict.py is in the same `app/` folder

app = FastAPI(
    title="Loan Approval Prediction API",
    description="Serves predictions based on user input and model selection logic",
    version="1.0.0"
)

# Allow all origins for development (you can restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the route
app.include_router(predict.router)
