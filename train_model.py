import logging
from pathlib import Path  
from src.data_loader import load_data
from src.pipelines    import build_pipelines
from src.train       import prepare_data, train, evaluate
from src.save        import save
from src.transformation import supprimer_doublons, filtre_ptid,nettoyer_diagnosis,remplacer_valeurs_invalides,convertir_taille_poids


meilleur_score    = 0


log = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("training.log")]
)

if __name__ == "__main__":
    log.info("========== DEBUT DE L'ENTRAINEMENT ==========")
    df = load_data()
    df = remplacer_valeurs_invalides(df)
    df = supprimer_doublons(df)
    df = filtre_ptid(df)
    df = convertir_taille_poids(df)
    df = nettoyer_diagnosis(df)
    X_train, X_test, y_train, y_test = prepare_data(df)
    pipelines                        = build_pipelines()    

    for model, pipeline in pipelines.items():
        log.info("--- Modèle : %s ---", model)
        pipeline = train(pipeline, X_train, y_train)
        metrics  = evaluate(pipeline, X_test, y_test)
        save(pipeline, metrics, model) 
    
        if metrics["f1-score_1"] > meilleur_score:
            meilleur_score    = metrics["f1-score_1"]
            meilleur_model      = model
            meilleur_pipeline = pipeline

    Path("artifacts/meilleur_model.txt").write_text(meilleur_model)
    log.info("Meilleur modèle : %s (f1-score_1=%.4f)", meilleur_model, meilleur_score)

    log.info("========== ENTRAINEMENT TERMINE ==========")