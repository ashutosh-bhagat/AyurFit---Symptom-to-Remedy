# 🌿 AyurFit — AI-Powered Ayurvedic Healthcare Assistant

> **Live Demo:** [ayur-fit-symptom-to-remedy.vercel.app](https://ayur-fit-symptom-to-remedy.vercel.app)
> **Backend API:** [ashutoshbhagat-ayurfit.hf.space/docs](https://ashutoshbhagat-ayurfit.hf.space/docs)

AyurFit bridges modern Natural Language Processing (NLP) with ancient Ayurvedic clinical practice — mapping patient symptoms and demographics to traditional Ayurvedic prescriptions through a **Two-Tier Machine Learning Architecture**.

---

## 🏗️ Architecture

```
User Browser
     │
     ▼
┌─────────────────────────────┐
│   Frontend (Vercel)          │   Next.js 16 / React 19
│   ayur-fit-symptom-to-       │   Tailwind CSS v4, Radix UI
│   remedy.vercel.app          │
└──────────────┬──────────────┘
               │ HTTPS POST /analyze
               ▼
┌─────────────────────────────┐
│   Backend (HuggingFace       │   FastAPI + Python
│   Spaces — Docker)           │   ML: scikit-learn, sentence-transformers
│   ashutoshbhagat-ayurfit     │   Data: pandas, numpy, joblib
│   .hf.space                  │
└─────────────────────────────┘
```

---

## 🧠 The Two-Tier ML Pipeline

### Tier 1 — Disease Prediction
- User's free-form symptom text is embedded using **`SentenceTransformer (all-MiniLM-L6-v2)`**
- A **`LinearSVC`** (Support Vector Machine) classifies the embedding into one of 14 disease groups
- A softmax-scaled confidence score is calculated from decision function values

### Tier 2 — Herbal Recommendation
- A **`DecisionTreeClassifier`** takes a 4-dimensional input: `[disease, severity, age, gender]`
- Outputs a personalized Ayurvedic herb formulation tailored to the user's demographic profile

### Knowledge Lookup
- The backend queries a **1,300-row Ayurvedic dataset** to append:
  - Sanskrit/Hindi disease name
  - Dosha imbalance (Vata / Pitta / Kapha)
  - Dietary recommendations
  - Yoga & physical therapy suggestions

---

## 🎯 API Response Example

**POST** `https://ashutoshbhagat-ayurfit.hf.space/analyze`

```json
// Request
{
  "symptoms": "severe headache and high fever since 2 days with body pain",
  "severity": 70,
  "age": 25,
  "gender": "male"
}

// Response
{
  "disease": "Infectious & Parasitic Diseases",
  "sanskritName": "सामान्य सर्दी",
  "doshas": "Kapha, Vata",
  "herbs": "Tulsi, Giloy, Neem",
  "diet": "Rest well; consume warm foods; avoid dairy temporarily.",
  "yoga": "Pranayama, Anulom Vilom",
  "confidence": 0.71
}
```

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend Framework** | Next.js 16 / React 19 (App Router) |
| **Styling** | Tailwind CSS v4 + custom design system |
| **UI Components** | Radix UI primitives, Lucide React icons |
| **Backend Framework** | FastAPI (Python) |
| **NLP Model** | `sentence-transformers/all-MiniLM-L6-v2` |
| **ML Models** | `scikit-learn` — LinearSVC, DecisionTreeClassifier |
| **Data Engineering** | `pandas`, `numpy`, `joblib` |
| **Containerization** | Docker (multi-stage build) |
| **Frontend Hosting** | Vercel |
| **Backend Hosting** | HuggingFace Spaces (Docker, CPU Basic) |

---

## 📁 Project Structure

```text
AyurFit---Symptom-to-Remedy/
│
├── backend/                          # FastAPI & Machine Learning Core
│   ├── dataset/
│   │   └── ayurfit_final.csv         # Master Dataset (1,300 Ayurvedic conditions)
│   ├── model/
│   │   ├── sys-dis imp files/
│   │   │   ├── tier1_svm_model.joblib        # Trained LinearSVC
│   │   │   └── disease_label_encoder.joblib  # Disease class encoder
│   │   ├── dis-rem imp files/
│   │   │   ├── tier2_recommender.joblib      # Trained DecisionTree
│   │   │   └── herbs_label_encoder.joblib    # Herbs class encoder
│   │   ├── symtom-disease.ipynb      # Tier 1 SVM Training Notebook
│   │   └── disease-remedie.ipynb     # Tier 2 DT Training Notebook
│   ├── main.py                       # FastAPI server (Two-Tier ML pipeline)
│   ├── requirements.txt              # Pinned Python dependencies
│   ├── Dockerfile                    # Multi-stage Docker build for HF Spaces
│   ├── .dockerignore                 # Excludes dev files from Docker image
│   └── upload_to_hf.py              # Utility: upload backend to HF Spaces
│
├── frontend/                         # Next.js Application
│   ├── app/
│   │   ├── globals.css               # Global styles & design tokens
│   │   ├── layout.jsx                # Root layout with theme provider
│   │   └── page.jsx                  # Main interactive dashboard
│   ├── components/
│   │   ├── header.jsx                # App header with navigation
│   │   ├── symptom-input.jsx         # Symptom text + Age/Gender/Severity inputs
│   │   ├── clinical-card.jsx         # Full clinical assessment results card
│   │   ├── herbal-recommendations.jsx # Tier 2 botanical UI
│   │   ├── confidence-gauge.jsx      # ML confidence score visualizer
│   │   ├── herb-illustrations.jsx    # Decorative SVG herb illustrations
│   │   ├── theme-provider.jsx        # Dark/light mode provider
│   │   └── theme-toggle.jsx          # Dark/light mode toggle button
│   ├── vercel.json                   # Vercel deployment configuration
│   ├── package.json                  # Node.js dependencies (pinned)
│   └── .env.example                  # Environment variable template
│
└── README.md
```

---

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+

### Step 1 — Start the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate       # Windows
# source .venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server (runs on http://127.0.0.1:8000)
python main.py
```

> **Note:** First startup downloads the `all-MiniLM-L6-v2` model (~90MB). Subsequent startups are instant.

### Step 2 — Configure Frontend Environment

```bash
cd frontend

# Copy the env template
cp .env.example .env.local

# .env.local content (for local dev — no changes needed):
# NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### Step 3 — Start the Frontend

```bash
cd frontend
npm install
npm run dev
# App available at http://localhost:3000
```

---

## ☁️ Deployment

### Backend → HuggingFace Spaces (Docker)

The backend runs in a Docker container on HuggingFace Spaces (CPU Basic, free tier).

**Key design decisions:**
- The `SentenceTransformer` model is **pre-downloaded at Docker build time** (not at runtime), eliminating cold-start delays
- Multi-stage Docker build keeps the final image lean
- Binary model files (`.joblib`, `.csv`) are tracked via Git LFS / HF Xet Storage

To redeploy the backend after changes:
```python
# Update upload_to_hf.py with a new HF Write token, then:
python backend/upload_to_hf.py
```

### Frontend → Vercel

The Next.js frontend is deployed on Vercel with automatic GitHub CI/CD.

Every push to `main` triggers a new Vercel deployment automatically.

**Required environment variable in Vercel:**
```
NEXT_PUBLIC_API_URL = https://ashutoshbhagat-ayurfit.hf.space
```

---

## ⚠️ HuggingFace Free Tier — Sleep Behaviour

On the free tier, HuggingFace Spaces sleep after ~48 hours of inactivity.

- **Impact:** The first request after sleep takes 30–60 seconds (cold start)
- **Fix:** Set up a free cron job at [cron-job.org](https://cron-job.org) to ping `https://ashutoshbhagat-ayurfit.hf.space/docs` every 30 minutes

---

## 📊 Dataset

`ayurfit_final.csv` — **1,300 unique clinical conditions** mapped across Ayurvedic categories:
- Dosha classifications (Vata, Pitta, Kapha, combinations)
- Botanical formulations and herb recommendations
- Diet & lifestyle recommendations
- Yoga & physical therapy regimens
- Demographic splits (age groups, gender)

---

## 📝 Disclaimer

This is an experimental AI-powered research tool for educational purposes. The recommendations generated are based on traditional Ayurvedic texts and ML pattern matching — they are **not a substitute for professional medical advice**. Always consult a qualified Ayurvedic practitioner (Vaidya) or licensed medical doctor before starting any treatment or consuming botanical remedies.