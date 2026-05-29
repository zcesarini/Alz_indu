# Projet Alzheimer

## Vue d'ensemble

Ce dépôt contient un pipeline ML pour un cas Alzheimer avec preprocessing, modelisation, serialisation des artefacts et interface web de pilotage.

Ce projet n'est plus limité aux notebooks. Il peut maintenant être utilise comme une petite application operationnelle pour :

- lancer une prediction unitaire via formulaire.

## Structure principale

- `train_model.py` : script principal d'entrainement, d'évaluation, comparaison et sauvegarde.
- `comparatif_model.py` : graphique de comparaison des metrics.
- `frontend/frontend.py` : serveur web local de l'interface applicative.
- `backend/backend.py` : API FastAPI permettant de charger le modèle de machine learning et d’effectuer les prédictions de risque de maladie d’Alzheimer.
- `src/config.py` : contient les constantes globales du projet :
  - chemin du dossier des artefacts (`ARTIFACTS`)
  - variable cible du modèle (`TARGET`)
  - paramètres de séparation des données (`TEST_SIZE`, `RANDOM_STATE`)
  - liste des variables explicatives utilisées pour l’entraînement du modèle (`FEATURES`)
- `src/data_loader.py` : chargement et récupération des données préprocessées depuis Supabase.
- `artifacts/` : modèles sérialises, métadonnées JSON, courbes d’apprentissage et matrices de confusion.

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
Ouvrir docker desktop

```powershell
docker compose up -d --build  
```
L'application sera accessible sur :

- Frontend Streamlit : http://localhost:8501
- API FastAPI : http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs

## Interface web

L'interface propose 4 zones principales :

- `Scores cognitifs` 
- `Signes vitaux et mesures`
- `Mesures biologiques`
- `Prediction unitaire`

## Dependances

Les dépendances applicatives sont déclarees dans `requirements.txt`.

## Notes

- Le dernier modèle disponible est détecté automatiquement depuis le fichier `meilleur_model.txt` enregistré pendant l'entraînement.

