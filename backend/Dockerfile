FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/backend.py .
COPY src/transformation.py ./src/transformation.py
COPY src/pipelines.py ./src/pipelines.py
COPY src/config.py ./src/config.py
COPY src/__init__.py ./src/__init__.py
COPY artifacts/meilleur_model.txt ./artifacts/meilleur_model.txt
COPY artifacts/*.joblib ./artifacts/

EXPOSE 8000

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
