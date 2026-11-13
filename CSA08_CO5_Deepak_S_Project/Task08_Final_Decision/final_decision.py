from pathlib import Path
import sys,sqlite3,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import load_and_clean,create_db
root=Path(__file__).resolve().parents[1]
rows,_=load_and_clean(root/"sample_air_quality.csv")
con=create_db(rows,root/"air_quality.sqlite")
query="SELECT AVG(pm25) FROM readings WHERE station=? AND day BETWEEN ? AND ?"
args=("Adyar","2026-10-01","2026-10-31")
t=time.perf_counter()
for _ in range(100): con.execute(query,args).fetchone()
before=time.perf_counter()-t
con.execute("CREATE INDEX IF NOT EXISTS idx_station_day ON readings(station,day)"); con.commit()
t=time.perf_counter()
for _ in range(100): con.execute(query,args).fetchone()
after=time.perf_counter()-t
print(f"100 query runs before index: {before:.6f}s")
print(f"100 query runs after index:  {after:.6f}s")
print("Index:",con.execute("PRAGMA index_list(readings)").fetchall())
print("Decision: retain SQLite with station/day index; validate and normalise at ingestion; batch and aggregate with SQL; use lexicon AI for triage only and a reviewed trained model for production sentiment.")
con.close()
