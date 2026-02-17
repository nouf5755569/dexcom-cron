import os
import json
import logging
from datetime import datetime, timezone

from dotenv import load_dotenv

from app.dexcom_client import DexcomClient
from app.storage import init_db, upsert_glucose_readings
from app.model_infer import maybe_run_model_inference

def setup_logging():
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def main():
    load_dotenv()
    setup_logging()
    log = logging.getLogger("cron")

    db_path = os.getenv("DB_PATH", "data/dexcom.sqlite")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    init_db(db_path)

    client = DexcomClient()

    log.info("Starting Dexcom pull...")
    readings = client.fetch_latest_glucose(max_count=36)  # تقريبًا 3 ساعات لو كل 5 دقائق
    log.info("Fetched %d glucose readings", len(readings))

    inserted = upsert_glucose_readings(db_path, readings)
    log.info("DB upsert complete. New/updated rows: %d", inserted)

    # Optional: model inference
    result = maybe_run_model_inference(db_path)
    if result is not None:
        log.info("Model inference result: %s", json.dumps(result, ensure_ascii=False))

    log.info("Done ✅ at %s", datetime.now(timezone.utc).isoformat())

if __name__ == "__main__":
    main()
