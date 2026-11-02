from app.database.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    print("DB result:", db.execute(text("SELECT 1")).scalar_one())
finally:
    db.close()
