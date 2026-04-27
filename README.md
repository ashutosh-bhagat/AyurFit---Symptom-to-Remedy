# 🌿 AyurFit - Two-Tier ML Ayurvedic Healthcare Assistant

AyurFit is a full-stack, AI-powered Ayurvedic health assistant. It utilizes a highly advanced **Two-Tier Machine Learning Architecture** via a FastAPI backend to map patient symptoms and demographics to traditional Ayurvedic prescriptions, delivered through a stunning Next.js user interface.

## 🎯 Project Overview

AyurFit bridges modern Natural Language Processing (NLP) with ancient Ayurvedic clinical practice:
- **Tier 1 (Disease Prediction):** Uses `SentenceTransformer (all-MiniLM-L6-v2)` embeddings and a `LinearSVC` (Support Vector Machine) to semantically analyze free-form symptom descriptions and accurately predict the underlying condition and dosha.
- **Tier 2 (Herbal Recommendation):** Uses a transparent `DecisionTreeClassifier` that takes the Tier 1 disease, along with user-reported **Severity, Age, and Gender**, to prescribe highly specific, personalized botanical formulations.
- **Dynamic UI:** Features a gorgeous Next.js frontend with glassmorphism, dynamic animations, and beautifully segmented clinical prescriptions (including Sanskrit naming and Dosha targeting).

## 🏗️ Tech Stack

### Frontend
- **Framework:** Next.js 16 / React 19 (App Router)
- **Styling:** Tailwind CSS v4 + custom design system
- **UI Components:** Radix UI primitives, Lucide React icons

### Backend & Machine Learning
- **API Framework:** FastAPI (Python)
- **NLP Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Predictive Models:** `scikit-learn` (LinearSVC, DecisionTreeClassifier)
- **Data Engineering:** `pandas`, `numpy`, `joblib`

## 📁 Project Structure

```text
AyurFit/
├── backend/                     # FastAPI & Machine Learning Core
│   ├── dataset/
│   │   └── final ayurfit.csv    # Master Dataset (1300+ Ayurvedic conditions)
│   ├── model/
│   │   ├── train_tier1_model.ipynb   # SVM Training Pipeline
│   │   ├── evaluate_tier1.ipynb      # K-Fold Cross Validation testing
│   │   ├── train_tier2_model.ipynb   # Decision Tree Demographic Training
│   │   └── *.joblib                  # Serialized Production Models
│   └── main.py                  # The robust FastAPI server
│
├── frontend/                    # Next.js Application
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.jsx
│   │   └── page.jsx             # Main interactive dashboard
│   ├── components/
│   │   ├── symptom-input.jsx           # Captures Symptoms, Age, Gender, Severity
│   │   ├── clinical-card.jsx           # Renders the full clinical assessment
│   │   └── herbal-recommendations.jsx  # Dedicated Tier 2 Botanical UI
│   └── package.json
│
└── README.md
```

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- Node.js 18+

### Step 1: Start the Backend (FastAPI)
Open a terminal and start the Python API:
```bash
cd backend
# Optional: create a virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Start the server
python .\main.py
# (Or use: uvicorn main:app --reload)
```
The backend initializes the Two-Tier ML brain at **http://127.0.0.1:8000**. 
*Note: The first startup will download the NLP SentenceTransformer.*

### Step 2: Start the Frontend (Next.js)
Open a **new terminal**:
```bash
cd frontend
npm install
npm run dev
```
The frontend UI starts at **http://localhost:3000**.

### Step 3: Use the App
1. Navigate to http://localhost:3000.
2. Enter your precise symptoms (e.g., "severe headache and blurry vision").
3. Adjust the **Age, Gender, and Severity** sliders.
4. Click "Botanical Scan" to trigger the ML pipeline.

## 🧠 The Two-Tier ML Pipeline

1. **Preprocessing:** The API safely maps the frontend UI's continuous sliders into categorical demographic bins (e.g., `Age=35` -> `Adult (2)`, `Gender=Male` -> `Male (1)`).
2. **Tier 1 Classification:** The user's unstructured symptom string is embedded via NLP and fed into the `LinearSVC`. The model outputs a predicted `disease` and a calculated `confidence score` (using softmax decision thresholds).
3. **Tier 2 Recommendation:** The `DecisionTreeClassifier` ingests a 4-dimensional matrix: `[[disease, severity, age, gender]]` to output a highly specific `Ayurvedic Herbs` prescription that accounts for the user's demographic profile.
4. **Knowledge Lookup:** The backend rapidly queries the Pandas DataFrame to append secondary holistic regimens (Sanskrit Name, Doshas, Diet, Yoga).

## 📊 The Dataset
The `final ayurfit.csv` comprises **1,300 unique clinical conditions** mapped extensively across Ayurvedic categories, detailing Doshas (Vata, Pitta, Kapha), Formulations, and deep Demographic splits.

## 📝 Disclaimer
This is an AI-generated experimental healthcare research tool. Always consult a qualified Ayurvedic practitioner (Vaidya) or medical doctor before starting any treatment or consuming botanical remedies.