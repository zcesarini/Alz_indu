# 1. Image Python officielle
FROM python:3.10-slim

# 2. Dossier de travail
WORKDIR /app

# 3. Copier les dépendances
COPY backend/requirements.txt .

# 4. Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier tout le backend
COPY backend/backend.py .
COPY src/transformation.py ./src/transformation.py
COPY src/pipelines.py ./src/pipelines.py
COPY src/config.py ./src/config.py
COPY src/__init__.py ./src/__init__.py
COPY artifacts/meilleur_model.txt ./artifacts/meilleur_model.txt
COPY artifacts/*.joblib ./artifacts/

# 6. Exposer le port FastAPI
EXPOSE 8000

# 7. Lancer FastAPI avec Uvicorn
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
