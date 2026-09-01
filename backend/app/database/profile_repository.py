import json
from app.database.connection import get_connection

def save_profile(profile: dict) -> dict:
    with get_connection() as db:
        db.execute("INSERT INTO profiles(id, payload) VALUES(1, ?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload, updated_at=CURRENT_TIMESTAMP", (json.dumps(profile),))
    return profile

def get_profile() -> dict | None:
    with get_connection() as db:
        row = db.execute("SELECT payload FROM profiles WHERE id=1").fetchone()
    return json.loads(row["payload"]) if row else None
