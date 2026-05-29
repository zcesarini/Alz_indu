from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI()


def get_latest_model():
    artifacts_path = Path("artifacts")
    meilleur_model   = (artifacts_path / "meilleur_model.txt").read_text()
    models = list(artifacts_path.glob(f"*_{meilleur_model}_model.joblib"))
    if not models:
        default = artifacts_path / "model.joblib"
        if default.exists():
            return joblib.load(default)
        raise FileNotFoundError("Aucun modèle trouvé.")
    latest = sorted(models, key=lambda x: int(x.stem.split("_")[0].replace("v", "")))[-1]
    return joblib.load(latest)

model = get_latest_model()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])

    if hasattr(model, "predict_proba"):
        raw_proba = model.predict_proba(df)
        if raw_proba.ndim == 2:
            proba = float(raw_proba[0][1] * 100)
        else:
            proba = float(raw_proba[1] * 100)
    else:
        raw = model.predict(df)
        proba = float(raw[0][0] * 100)

    prediction = int(model.predict(df)[0])

    return {
        "prediction": int(prediction),
        "probabilite": round(proba, 2)
    }
  