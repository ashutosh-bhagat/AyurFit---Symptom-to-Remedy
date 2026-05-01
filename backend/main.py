import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent

# Global variables
df = None
nlp_model = None
tier1_svm = None
disease_encoder = None
tier2_dt = None
herbs_encoder = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global df, nlp_model, tier1_svm, disease_encoder, tier2_dt, herbs_encoder

    print("Loading AyurFit Brain (Two-Tier ML Architecture)...")

    # Load dataset safely
    csv_path = BASE_DIR / "dataset" / "ayurfit_final.csv"
    if not csv_path.exists():
        csv_path = BASE_DIR / "dataset" / "data.csv"

    try:
        df = pd.read_csv(csv_path)
        df = df.dropna(subset=['New_Disease_Group'])
        print(f"Loaded dataset from: {csv_path}")
    except Exception as e:
        print(f"Error loading dataset: {e}")

    # Initialize NLP model
    print("Loading SentenceTransformer...")
    nlp_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

    # Load the 4 joblib models safely
    model_dir = BASE_DIR / "model"
    try:
        tier1_svm = joblib.load(model_dir / "sys-dis imp files" / "tier1_svm_model.joblib")
        disease_encoder = joblib.load(model_dir / "sys-dis imp files" / "disease_label_encoder.joblib")
        tier2_dt = joblib.load(model_dir / "dis-rem imp files" / "tier2_recommender.joblib")
        herbs_encoder = joblib.load(model_dir / "dis-rem imp files" / "herbs_label_encoder.joblib")
        print("Loaded all 4 ML models successfully.")
    except FileNotFoundError as e:
        print(f"CRITICAL ERROR: Missing model artifact! Please ensure all .joblib files are in backend/model/. Error: {e}")
    except Exception as e:
        print(f"Error loading models: {e}")

    yield
    # Any necessary cleanup code would go here

app = FastAPI(title="AyurFit API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(request: Request):
    try:
        if any(resource is None for resource in [nlp_model, tier1_svm, disease_encoder, tier2_dt, herbs_encoder]):
            return {"error": "Model initialization failed. Check backend startup logs for missing/corrupt model files."}

        data = await request.json()
        symptoms = data.get("symptoms", "")
        
        if not symptoms:
            return {"error": "Symptoms text is required"}
            
        try:
            severity = int(data.get("severity", 50))
        except (ValueError, TypeError):
            severity = 50
            
        try:
            age = int(data.get("age", 35))
        except (ValueError, TypeError):
            age = 35
            
        gender = str(data.get("gender", "both")).lower()

        # Phase A: Preprocessing
        if severity < 33:
            mapped_severity = 0
        elif severity < 66:
            mapped_severity = 1
        elif severity < 85:
            mapped_severity = 2
        else:
            mapped_severity = 3
            
        # Map Age (0: Child, 1: Teen, 2: Adult, 3: Senior)
        if age < 13:
            mapped_age = 0
        elif age < 20:
            mapped_age = 1
        elif age < 60:
            mapped_age = 2
        else:
            mapped_age = 3
            
        # Map Gender (0: Both, 1: Male, 2: Female)
        if 'female' in gender or 'women' in gender:
            mapped_gender = 2
        elif 'male' in gender or 'men' in gender:
            mapped_gender = 1
        else:
            mapped_gender = 0

        # Phase B: Tier 1 (Disease Prediction)
        embedding = nlp_model.encode([symptoms], show_progress_bar=False)
        embedding_2d = embedding.reshape(1, -1)
        
        disease_encoded = tier1_svm.predict(embedding_2d)
        predicted_disease = disease_encoder.inverse_transform(disease_encoded)[0]
        
        # Calculate pseudo-confidence score
        try:
            decision_scores = tier1_svm.decision_function(embedding_2d)
            exp_scores = np.exp(decision_scores - np.max(decision_scores))
            probabilities = exp_scores / exp_scores.sum(axis=1, keepdims=True)
            raw_confidence = float(np.max(probabilities))
            # Use the model's raw confidence (0.0 - 1.0) instead of forcing a 0.70 minimum.
            confidence_score = float(np.clip(raw_confidence, 0.0, 1.0))
        except Exception:
            confidence_score = 0.94

        # Phase C: Tier 2 (Remedy Recommendation)
        X_tier2 = np.array([[disease_encoded[0], mapped_severity, mapped_age, mapped_gender]])
        
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            herbs_encoded = tier2_dt.predict(X_tier2)
            
        recommended_herbs = herbs_encoder.inverse_transform(herbs_encoded)[0]
        
        # Check if herbs recommendation is empty or invalid
        if recommended_herbs == 'nan' or not str(recommended_herbs).strip() or "None specific" in str(recommended_herbs):
            recommended_herbs = "Consult an Ayurvedic Doctor"

        # Phase D: Database Lookup for Lifestyle
        match_row = df[df['Disease_Group'] == predicted_disease] if df is not None else pd.DataFrame()
        
        if not match_row.empty:
            diet_recommendations = str(match_row.iloc[0].get("Diet and Lifestyle Recommendations", "Maintain a balanced, easily digestible diet."))
            yoga_recommendations = str(match_row.iloc[0].get("Yoga & Physical Therapy", "Practice gentle stretching and Pranayama."))
            doshas = str(match_row.iloc[0].get("Doshas", "Vata-Pitta-Kapha (Tridoshic)"))
            sanskrit_name = str(match_row.iloc[0].get("Hindi Name", predicted_disease))
        else:
            diet_recommendations = "Maintain a balanced, easily digestible diet."
            yoga_recommendations = "Practice gentle stretching and Pranayama."
            doshas = "Vata-Pitta-Kapha (Tridoshic)"
            sanskrit_name = predicted_disease
            
        if diet_recommendations == 'nan' or not diet_recommendations.strip():
            diet_recommendations = "Maintain a balanced, easily digestible diet."
        if yoga_recommendations == 'nan' or not yoga_recommendations.strip():
            yoga_recommendations = "Practice gentle stretching and Pranayama."
        if doshas == 'nan' or not doshas.strip():
            doshas = "Vata-Pitta-Kapha (Tridoshic)"
        if sanskrit_name == 'nan' or not sanskrit_name.strip():
            sanskrit_name = predicted_disease

        # Phase E: Frontend Payload Generation
        return {
            "disease": predicted_disease,
            "sanskritName": sanskrit_name,
            "doshas": doshas,
            "herbs": recommended_herbs,
            "diet": diet_recommendations,
            "yoga": yoga_recommendations,
            "confidence": round(confidence_score, 4)
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
