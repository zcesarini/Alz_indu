# Projet Alzheimer

## Vue d'ensemble

Ce dépôt contient un pipeline ML pour un cas Alzheimer avec preprocessing, modelisation, serialisation des artefacts et interface web de pilotage.

Ce projet n'est plus limité aux notebooks. Il peut maintenant être utilise comme une petite application operationnelle pour :

- lancer une prediction unitaire via formulaire.
- et visualiser les dashboard Power BI des patients.

## Structure principale

Code
├── train_model.py           # Script principal : entraînement, évaluation, comparaison, sauvegarde
├── comparatif_model.py      # Graphique comparatif des performances des modèles
├── Docker-compose.yml       # Orchestration backend + frontend
├── requirements.txt         # Dépendances globales
│
├── backend/                 # API FastAPI pour la prédiction
│   ├── backend.py           # Endpoints /predict et /health
│   ├── Dockerfile           # Image Docker backend
│   └── requirements.txt     # Dépendances backend
│
├── frontend/                # Interface utilisateur Streamlit
│   ├── frontend.py          # UI : upload, prédiction, visualisation
│   ├── Dockerfile           # Image Docker frontend
│   └── requirements.txt     # Dépendances frontend
│
├── src/                     # Code métier (ML + preprocessing)
│   ├── config.py            # Constantes globales (ARTIFACTS, TARGET, FEATURES…)
│   ├── data_loader.py       # Chargement des données depuis Supabase
│   ├── pipelines.py         # Pipelines ML (scaling, encodage…)
│   ├── train.py             # Fonctions d'entraînement
│   ├── transformation.py    # Feature engineering / preprocessing
│   └── save.py              # Sauvegarde des modèles et métriques
│
├── artifacts/               # Artefacts générés automatiquement
│   ├── *_metrics.json       # Métriques des modèles
│   ├── *_confusion_matrix.png # Matrices de confusion
│   ├── *_learning_curve.png # Courbes d’apprentissage
│   ├── *.joblib             # Modèles ML sérialisés
│   ├── *.h5                 # Modèles Keras
│   └── meilleur_model.txt   # Nom du meilleur modèle sélectionné
│
└── README.md                # Documentation du projet


## Lancement rapide

1. Activer l'environnement virtuel :

```powershell
& ".venv\Scripts\Activate.ps1"
```

2. Installer les dependances :

```powershell
python -m pip install -r requirements.txt
```

3. Entrainer ou re-entrainer un modele :

```powershell
python train_model.py
```

4. Lancer le tableau de bord des metrics :

```powershell
python comparatif_model.py
```

5. Lancer l'interface :
## en ligne
https://alz-indu-frontend.onrender.com/  

Si message d'erreur relancer les services render :  
- backend (erreur à la prédiction)  https://dashboard.render.com/web/srv-d8crcu6k1jcs73a4h6vg 
- frontend (erreur au chargement de la page streamlit) https://dashboard.render.com/web/srv-d8cs776k1jcs73a5jq5g/settings  

## en local 
Ouvrir docker desktop

```powershell
docker compose up -d --build  
```
L'application sera accessible en local sur :

- Frontend Streamlit : http://localhost:8501
- API FastAPI : http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs

## Interface web

L'interface propose 5 zones principales :

- `Affichage du dashboard Power BI des patients` 
- `Scores cognitifs` 
- `Signes vitaux et mesures`
- `Mesures biologiques`
- `Prediction unitaire`

## Dependances

Les dépendances applicatives sont déclarees dans `requirements.txt`.

## Notes

- Le dernier modèle disponible est détecté automatiquement depuis le fichier `meilleur_model.txt` enregistré pendant l'entraînement.

