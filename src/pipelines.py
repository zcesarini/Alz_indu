import logging
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from scikeras.wrappers import KerasClassifier
from tensorflow import keras
from tensorflow.keras import layers
from src.config import RANDOM_STATE
from src.transformation import  calculer_indicateurs, garder_colonnes_finales

log = logging.getLogger(__name__)

def build_nn(input_shape=(19,)):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(32, activation="relu"),
        layers.Dense(16, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ])
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model


    
def build_pipelines() -> dict:
    log.info("Construction des pipelines")
    steps_communs = [
        ("calculer_indicateurs", FunctionTransformer(calculer_indicateurs)),
        ("garder_colonnes_finales", FunctionTransformer(garder_colonnes_finales)),
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ]
    
    return {
        "random_forest": Pipeline(steps=steps_communs + [
            ("model", RandomForestClassifier(
                n_estimators=200,
                min_samples_split=5,
                min_samples_leaf=2,
                class_weight="balanced",
                random_state=RANDOM_STATE,
                n_jobs=-1
            ))
        ]),
        "gradient_boosting": Pipeline(steps=steps_communs + [
            ("model", GradientBoostingClassifier(random_state=RANDOM_STATE))
        ]),
        "Keras_classifier": Pipeline(steps=steps_communs + [
        ("model", KerasClassifier(
            model=build_nn,
            epochs=20,
            batch_size=32,
            verbose=0))
        ]),
    }
