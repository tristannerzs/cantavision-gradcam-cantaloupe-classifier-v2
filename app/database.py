import csv, io, sqlite3
from contextlib import contextmanager
from typing import Iterator, Any
from .settings import DB_DIR
DB_PATH = DB_DIR / "predictions.sqlite3"
SCHEMA = """
CREATE TABLE IF NOT EXISTS predictions (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 created_at TEXT NOT NULL DEFAULT (datetime('now')),
 filename TEXT NOT NULL,
 model_name TEXT NOT NULL,
 mode TEXT NOT NULL,
 roi_x INTEGER NOT NULL, roi_y INTEGER NOT NULL, roi_w INTEGER NOT NULL, roi_h INTEGER NOT NULL,
 predicted_label TEXT NOT NULL,
 probability_cantaloupe REAL NOT NULL,
 probability_not_cantaloupe REAL NOT NULL,
 confidence REAL NOT NULL,
 threshold REAL NOT NULL,
 gradcam_status TEXT NOT NULL,
 gradcam_layer TEXT,
 crop_image TEXT,
 heatmap_image TEXT,
 smooth_heatmap_image TEXT,
 overlay_image TEXT,
 study_panel_image TEXT
);
"""
@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
def insert(row: dict[str, Any]) -> int:
    init_db(); cols = list(row.keys())
    with connect() as conn:
        cur = conn.execute(f"INSERT INTO predictions ({','.join(cols)}) VALUES ({','.join(':'+c for c in cols)})", row)
        return int(cur.lastrowid)
def recent(limit: int = 18) -> list[dict[str, Any]]:
    init_db(); limit=max(1,min(int(limit),500))
    with connect() as conn:
        rows = conn.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]
def stats() -> dict[str, Any]:
    init_db()
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        cant = conn.execute("SELECT COUNT(*) FROM predictions WHERE predicted_label='cantaloupe'").fetchone()[0]
        avg = conn.execute("SELECT AVG(confidence) FROM predictions").fetchone()[0]
    return {"total": int(total or 0), "cantaloupe": int(cant or 0), "not_cantaloupe": int((total or 0)-(cant or 0)), "avg_confidence": float(avg or 0)}
def csv_export() -> str:
    rows=recent(100000)
    fields=["id","created_at","filename","model_name","mode","roi_x","roi_y","roi_w","roi_h","predicted_label","probability_cantaloupe","probability_not_cantaloupe","confidence","threshold","gradcam_status","gradcam_layer","crop_image","heatmap_image","overlay_image","study_panel_image"]
    out=io.StringIO(); w=csv.DictWriter(out, fieldnames=fields); w.writeheader()
    for row in rows: w.writerow({f: row.get(f,"") for f in fields})
    return out.getvalue()
