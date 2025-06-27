# 🚀 Loan Approval Predictor

A full-stack AI-powered web application that predicts loan approval decisions using both applicant-level (micro) data and live macroeconomic indicators like GDP growth, inflation, interest rate, and employment rate via the FRED API.

## 📸 Demo
- **Live App**: [mrloanpredictor.vercel.app](https://mrloanpredictor.vercel.app)

## 🧠 Features
- ✅ Micro-Level Prediction using applicant data
- ✅ Macro-Level Switch: Model uses macroeconomic indicators when relevant
- ✅ FRED API Integration for live interest, inflation, GDP, employment data
- ✅ Cyberpunk-themed UI with responsive design
- ✅ Real-time predictions with confidence score
- ✅ Model Explainability Logic (optional, toggleable)
- ✅ Fully containerized backend/frontend separation

## 📦 Tech Stack
| Layer         | Technology                              |
|---------------|-----------------------------------------|
| Frontend      | React, Vite, Tailwind CSS              |
| Backend       | FastAPI, Uvicorn                       |
| ML Model      | XGBoost (saved as JSON)                |
| Data API      | FRED (Federal Reserve Economic Data)   |
| Hosting       | Vercel (frontend), Render (backend)    |
| Env Management| .env via Vercel & Render dashboards    |

## 🧮 Model Logic
The system uses two models:
- `model_basic.json`: Uses only applicant features.
- `model_macro.json`: Includes macroeconomic indicators.

**Macro model triggers when**:
- Loan amount ≥ ₹500,000
- Loan type is Home or Business
- Loan purpose is Business Expansion or Home Improvement

**Macroeconomic features** fetched via FRED:
- Interest Rate (FEDFUNDS)
- Unemployment Rate (UNRATE)
- Inflation Rate (CPIAUCSL)
- GDP Growth Rate (GDPC1)

## 🚀 Setup Instructions

### 🔧 Backend (FastAPI + XGBoost)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```ini
FRED_API_KEY=your_fred_api_key
```

Run the server:
```bash
uvicorn app.main:app --reload
```

### 🌐 Frontend (Vite + Tailwind CSS)
```bash
cd frontend
npm install
```

Create a `.env` file:
```ini
VITE_API_URL=https://your-backend-url.onrender.com
```

Run locally:
```bash
npm run dev
```

## 🌍 Deployment

### Backend (Render)
1. Upload the `backend` folder
2. Set Start Command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```
3. Add `FRED_API_KEY` in environment variables

### Frontend (Vercel)
1. Connect to `frontend` folder
2. Set Environment Variable:
   ```ini
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

## 🔐 Security Tips
- Do not commit `.env` files to GitHub
- Always add sensitive files to `.gitignore`
- Use Vercel/Render's dashboard to store keys securely

## ✨ Future Enhancements
- Add SHAP or LIME for explainability
- Add admin dashboard for monitoring predictions
- Add email/OTP verification for enterprise mode
- Model auto-retraining pipeline with CI/CD

## 🙌 Credits
- Created by Mohamed Roshan
- API Source: [FRED - Federal Reserve Economic Data](https://fred.stlouisfed.org/)
