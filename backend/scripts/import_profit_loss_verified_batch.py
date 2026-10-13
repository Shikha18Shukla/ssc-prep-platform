"""Idempotently validate/import the curated Profit & Loss question batch."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from app.database.session import SessionLocal, engine
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "profit_loss_verified_batch.json"

def main():
    engine.echo = False
    data = BATCH.read_bytes()
    with SessionLocal() as db:
        dry = import_questions(db, data, "application/json", BATCH.name, True)
        if dry.aborted or dry.errors:
            raise SystemExit(f"Validation failed; import not attempted: {dry.model_dump()}")
        print("DRY_RUN", dry.model_dump())
        result = import_questions(db, data, "application/json", BATCH.name, False)
        if result.aborted or result.errors:
            raise SystemExit(f"Import aborted: {result.model_dump()}")
        print("IMPORT", result.model_dump())

if __name__ == "__main__":
    main()
