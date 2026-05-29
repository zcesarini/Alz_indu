from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field

class PredictionData(BaseModel):
    CDGLOBAL: float = Field(example=0)
    CDMEMORY: float = Field(example=0)
    CDRSB: float = Field(example=0)
    CDJUDGE: float = Field(example=0)
    CDHOME: float = Field(example=0)
    CDCOMMUN: float = Field(example=0)

    MMSCORE: float = Field(example=29)
    TOTSCORE: float = Field(example=12)
    TOTAL13: float = Field(example=20)

    WORD2DL: float = Field(example=0)

    ST112SV: float = Field(example=4184.10)
    ST120SV: float = Field(example=6224)
    ST101SV: float = Field(example=1819.45)
    ST125SV: float = Field(example=24.50)

    VSWEIGHT: float = Field(example=94)
    VSHEIGHT: float = Field(example=170)

    VSBPSYS: float = Field(example=150)
    VSBPDIA: float = Field(example=64)

    VSPULSE: float = Field(example=64)

class PredictionResponse(BaseModel):
    prediction: int = Field(example=0)
    probabilite: float = Field(example=14.03)

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

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionData):
    df = pd.DataFrame([data.dict()])

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
  