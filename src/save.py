import json
import logging
import joblib
from pathlib import Path
from datetime import datetime
from sklearn.pipeline import Pipeline
from src.config import ARTIFACTS

log = logging.getLogger(__name__)



def save(pipeline: Pipeline, metrics: dict, model: str):
    ARTIFACTS.mkdir(exist_ok=True)
    version      = len(list(ARTIFACTS.glob(f"*model*.joblib"))) + 1
    model_path   = ARTIFACTS / f"v{version}_{model}_model.joblib"
    metrics_path = ARTIFACTS / f"v{version}_{model}_metrics.json"

    metrics["timestamp"] = datetime.now().isoformat()
    joblib.dump(pipeline, model_path)
    metrics_path.write_text(json.dumps(metrics,indent=2))

    log.info(f"Modele    :{model_path}")
    log.info(f"Metriques :{metrics_path}")

    for plot_name in ["confusion_matrix.png", "learning_curve.png"]:
        old_plot   = ARTIFACTS / plot_name
        new_plot = ARTIFACTS / f"v{version}_{model}_{plot_name.replace('.png', f'.png')}"
        old_plot.rename(new_plot)
