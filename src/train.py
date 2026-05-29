import logging
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from sklearn.model_selection import train_test_split, cross_val_score,learning_curve
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from src.config import FEATURES, TARGET, TEST_SIZE, RANDOM_STATE

log = logging.getLogger(__name__)

def prepare_data(df: "pd.DataFrame"):
    log.info("Split train/test")
    X = df[FEATURES]
    y = df[TARGET]
    return train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

def train(pipeline: Pipeline, X_train, y_train) -> Pipeline:
    log.info("Entraînement...")
          
    pipeline.fit(X_train, y_train)

    cv = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="accuracy")
    log.info(f"Cross-val : {cv.mean():.4f} ± {cv.std():.4f}")

    train_sizes, train_scores, val_scores = learning_curve(
        pipeline, X_train, y_train, cv=5, scoring="accuracy",
        train_sizes=np.linspace(0.1, 1.0, 10)
    )

    train_mean = train_scores.mean(axis=1)
    val_mean = val_scores.mean(axis=1)

    plt.figure(figsize=(7,5))
    plt.plot(train_sizes, train_mean, label="Score entraînement")
    plt.plot(train_sizes, val_mean, label="Score validation")
    plt.title("Courbe d’apprentissage")
    plt.xlabel("Taille du jeu d'entraînement")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    learning_curve_path = "artifacts/learning_curve.png"
    plt.savefig(learning_curve_path)
    plt.close()

    log.info(f"Courbe d’apprentissage sauvegardée : {learning_curve_path}")
    
    return pipeline

def evaluate(pipeline: Pipeline, X_test, y_test) -> dict:
    log.info("Évaluation sur le jeu de test")
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    metrics = {
        "precision_1": round(report["1"]["precision"], 4),
        "recall_1": round(report["1"]["recall"], 4),
        "f1-score_1": round(report["1"]["f1-score"], 4),
        "accuracy": round(report["accuracy"], 4)
    }
    
    log.info(f"\n{classification_report(y_test, y_pred)}")
    log.info(f"Matrice de confusion :\n{confusion_matrix(y_test, y_pred)}")

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Sain", "Malade"],
                yticklabels=["Sain", "Malade"])
    plt.title("Matrice de confusion")
    plt.xlabel("Prédiction")
    plt.ylabel("Réel")

    heatmap_path = "artifacts/confusion_matrix.png"
    plt.savefig(heatmap_path)
    plt.close()

    log.info(f"Matrice de confusion sauvegardée : {heatmap_path}")
    
    return metrics