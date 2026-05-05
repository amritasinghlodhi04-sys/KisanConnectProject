# 🌾 KisanConnect - AI/ML Intelligence Microservice

## 📖 Project Overview
KisanConnect is a price-aware, AI-informed direct agricultural marketplace. Its core mission is to eliminate the ₹32/kg intermediary price gap in India by connecting farmers directly with consumers and bulk buyers (B2B). 

This repository houses the **Machine Learning & Intelligence Microservice**, built using Python and FastAPI. It acts as the "brain" of KisanConnect, responsible for:
*   **Dynamic Fair Price Engine:** Recommending data-driven listing prices.
*   **Demand Forecasting:** Predicting crop trends in regional hubs like Bhopal, Damoh, and Bengaluru.
*   **Voice & NLP:** Processing Hindi/Hinglish voice input for illiterate or tech-novice farmers.
*   **Trust & Scoring:** Calculating farmer reputation and micro-credit risk profiles.
*   **Sustainability:** Generating carbon footprint tags and nutritional data.

---

## 🏗️ Project Structure & File Details

This project uses a modular, microservice-ready architecture. Below is the exact blueprint of the repository and the purpose of every file.

    kisanconnect-ml/
    ├── .vscode/                     # VSCode configuration folder
    │   ├── launch.json              # Config to run the FastAPI debugger in VSCode (Hit F5)
    │   └── settings.json            # Enforces Python formatting (Black) and environment paths
    ├── api/                         # The routing layer (API Endpoints)
    │   ├── __init__.py              # Marks directory as a Python package
    │   └── routers/                 # Groups endpoints by feature domain
    │       ├── __init__.py
    │       ├── pricing.py           # Handles /price-recommend and /demand-forecast
    │       ├── farmer.py            # Handles /reputation-score, /credit-profile, /farmer-clusters
    │       ├── nlp.py               # Handles /crop-classify (Hindi NLP via spaCy)
    │       └── sustainability.py    # Handles /carbon-estimate and /nutrition-lookup
    ├── core/                        # Application-wide settings
    │   ├── __init__.py
    │   └── config.py                # Loads environment variables (API keys, DB URIs) from a .env file
    ├── models/                      # Pydantic schemas for Data Validation
    │   ├── __init__.py
    │   └── schemas.py               # Defines the exact JSON structure required for API inputs/outputs
    ├── services/                    # The Business Logic Layer (Where API meets ML)
    │   ├── __init__.py
    │   ├── model_service.py         # Loads .pkl files and runs predictions/inference
    │   └── rag_service.py           # Handles LangChain/FAISS logic for scheme & advisory queries
    ├── notebooks/                   # Data Science Workspace
    │   └── model_training_and_eda.py # Scripts/Notebooks for cleaning data and training models
    ├── saved_models/                # IMPORTANT: Directory for compiled ML models (.pkl files)
    │   └── .gitkeep                 # (Note: .pkl files are often ignored in git due to size)
    ├── main.py                      # The entry point of the FastAPI application
    ├── requirements.txt             # Strict list of all Python dependencies and their versions
    └── README.md                    # This master documentation file

### Why are some files "missing"?
*   **`.pkl` files in `saved_models/`:** Machine learning models (like Random Forest or Prophet models) are large binary files. They are generated locally by running the scripts in the `/notebooks` folder and are purposely not uploaded to version control (Git) to save space.
*   **`.env` file:** This file holds secret keys. It is never pushed to the repository for security reasons. You must create it locally.

---

## 🚀 Setup & Installation (Step-by-Step)

Follow these steps exactly to run the project on any new machine (Windows, Mac, or Linux).

### Step 1: Clone the Repository
Download the code to your local machine.
    
    git clone <your_repository_url_here>
    cd kisanconnect-ml

### Step 2: Create a Virtual Environment
A virtual environment isolates this project's dependencies from the rest of your computer. 
*Note: This project requires Python 3.11.*

**For Windows:**
    
    python -m venv .env
    .env\Scripts\activate

**For macOS / Linux:**
    
    python3.11 -m venv .env
    source .env/bin/activate

*(Success Check: You should see `(.env)` appear at the beginning of your terminal prompt).*

### Step 3: Install Required Dependencies
Install the required packages (FastAPI, Scikit-learn, LangChain, etc.) and download the Hindi language model for spaCy.
    
    pip install --upgrade pip
    pip install -r requirements.txt
    python -m spacy download hi_core_news_sm

---

## ⚡ Running the Application

Once your environment is set up and activated, start the FastAPI server using `uvicorn`.

    uvicorn main:app --reload

*   `main:app` tells Uvicorn to look in `main.py` for the `app` object.
*   `--reload` enables auto-reloading. If you save a change in your code, the server restarts automatically.

**Accessing the APIs:**
*   **Base URL:** `http://127.0.0.1:8000`
*   **Interactive Documentation (Swagger UI):** `http://127.0.0.1:8000/docs` *(Use this interface to test all APIs directly from your browser!)*
*   **Alternative Docs (ReDoc):** `http://127.0.0.1:8000/redoc`

---

## 🌐 API Documentation

Below is the exhaustive list of available microservice endpoints. 

| Method | Endpoint | Description | Required Input Payload (JSON) | Expected Output Response (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/ml/price-recommend` | Suggests an optimal listing price range using a trained Regression Model. | `{"crop": "Tomato", "district": "Bhopal", "season": "Rabi", "rainfall_mm": 120.5}` | `{"min_price": 18, "max_price": 24}` |
| **GET** | `/ml/demand-forecast` | Predicts future demand trends using Facebook Prophet time-series forecasting. | **Query Params:** `?crop_id=101&days_ahead=7` | `{"crop_id": "101", "forecast": [{"date":"2026-05-06", "trend": "up"}]}` |
| **POST** | `/ml/reputation-score` | Computes farmer trust score using Bayesian smoothing logic. | `{"delivery_success_rate": 0.95, "avg_rating": 4.5, "disputes": 0}` | `{"score": 4.8, "tier": "Top Rated"}` |
| **POST** | `/ml/crop-classify` | Extracts crop info from Hindi text/voice transcripts using spaCy. | `{"voice_transcript": "मुझे पचास किलो प्याज बेचना है"}` | `{"crop_name": "प्याज", "quantity_kg": 50}` |
| **POST** | `/ml/credit-profile` | Classifies a farmer's credit risk to pre-approve micro-loans. | `{"revenue_history": [5000, 7000, 6500], "reputation_score": 4.8}` | `{"risk_tier": "low", "approved": true}` |
| **POST** | `/ml/carbon-estimate` | Estimates transport emissions from farm to buyer. | `{"farm_lat": 23.83, "farm_lon": 79.44, "buyer_lat": 12.97, "buyer_lon": 77.59, "weight_kg": 500}`| `{"emissions_kg_co2": 4.2}` |
| **POST** | `/ml/nutrition-lookup` | Returns AI-generated nutritional estimates per crop variety. | `{"crop_variety": "Desi Tomato"}` | `{"kcal": 18, "vitamins": ["C", "K"]}` |
| **GET** | `/ml/farmer-clusters` | Groups geographically/categorically similar farmers for Co-op/bulk selling (K-Means). | **Query Params:** `?region=Karnataka` | `{"clusters": [{"cluster_id": 1, "size": 15}]}` |

### 🧪 How to Use/Test an API (Example)
If someone else (like your Frontend or Backend team) needs to connect to this ML service, they can test it using Python's `requests` library:

    import requests

    url = "http://127.0.0.1:8000/ml/price-recommend"
    payload = {
        "crop": "Onion",
        "district": "Bengaluru",
        "season": "Rabi",
        "rainfall_mm": 45.5
    }

    response = requests.post(url, json=payload)
    print(response.json()) 
    # Output: {'min_price': 22.0, 'max_price': 28.0}

---

## 🛠️ ML Developer Workflow (How to Train and Deploy a New Model)

If you are developing a new Machine Learning model (e.g., the Price Prediction model) and want to expose it via the API, follow these exact steps:

### Step 1: Train and Save the Model locally
Open your terminal, ensure your virtual environment is active, and run the training script located in the `notebooks` folder:

    python notebooks/model_training_and_eda.py

Inside that file, the code will load data, train the model, and serialize it into a `.pkl` file using `pickle`. *Here is what the inside of that script looks like:*

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# 1. Load your dataset
df = pd.read_csv('data/agmarknet_prices.csv')
X = df[['rainfall', 'season_encoded']]
y = df['price']

# 2. Train the model
model = RandomForestRegressor()
model.fit(X, y)

# 3. Serialize and save the model to the saved_models folder
with open('../saved_models/price_model.pkl', 'wb') as file:
    pickle.dump(model, file)