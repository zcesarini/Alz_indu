import logging
import pandas as pd
from src.config import FEATURES, TARGET
import os
from supabase import create_client

log = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_data() -> pd.DataFrame:
    log.info(f"Chargement des données depuis SUPABASE...")
    batch_size=1000
    rows = []
    start = 0

    while True:
        end = start + batch_size - 1
        batch = supabase.table("ALZ_BRONZE").select("*").range(start, end).execute()

        if not batch.data:
            break

        rows.extend(batch.data)
        start += batch_size

    df = pd.DataFrame(rows)

    log.info(f"Table ALZ_BRONZE chargée : {df.shape[0]:,} lignes × {df.shape[1]} colonnes")
    
    return df






