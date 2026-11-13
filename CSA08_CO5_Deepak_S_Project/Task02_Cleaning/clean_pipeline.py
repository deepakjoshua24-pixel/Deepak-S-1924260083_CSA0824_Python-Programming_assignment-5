from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import load_and_clean, create_db
root=Path(__file__).resolve().parents[1]
rows,rejected=load_and_clean(root/"sample_air_quality.csv")
print("Rows cleaned:",len(rows))
print("Rejected malformed rows:",len(rejected))
print("First 3 cleaned rows:")
for r in rows[:3]: print(r)
con=create_db(rows,root/"air_quality.sqlite")
print("SQLite rows:",con.execute("SELECT COUNT(*) FROM readings").fetchone()[0])
print("Adyar October mean PM2.5:",round(con.execute("SELECT AVG(pm25) FROM readings WHERE station=? AND day LIKE ?",("Adyar","2026-10-%")).fetchone()[0],2))
con.close()
