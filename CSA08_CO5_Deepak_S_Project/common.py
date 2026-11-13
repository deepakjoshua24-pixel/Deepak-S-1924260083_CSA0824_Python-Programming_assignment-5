import csv, sqlite3, statistics, re, os
from collections import defaultdict, Counter
from datetime import datetime

VALID_RANGES = {"pm25": (0, 999), "pm10": (0, 2000), "no": (0, 1000), "temperature": (-20, 60)}
def load_and_clean(path):
    cleaned=[]; rejected=[]
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        required={"station","date","hour","pm25","pm10","no","temperature"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("CSV is missing one or more required columns")
        for line,row in enumerate(reader, start=2):
            try:
                station=row["station"].strip().title()
                day=datetime.strptime(row["date"].strip(), "%Y-%m-%d").date().isoformat()
                hour=int(row["hour"])
                if not 0 <= hour <= 23: raise ValueError("hour out of range")
                vals={}
                for col in ("pm25","pm10","no","temperature"):
                    raw=(row[col] or "").strip()
                    vals[col]=None if raw.upper() in ("","NA","N/A","NULL") else float(raw)
                if station in ("Thiruvanmiyur","Porur") and vals["temperature"] is not None:
                    vals["temperature"]=(vals["temperature"]-32)*5/9
                for col,(lo,hi) in VALID_RANGES.items():
                    v=vals[col]
                    if v is not None and not lo <= v <= hi: vals[col]=None
                cleaned.append((station,day,hour,vals["pm25"],vals["pm10"],vals["no"],vals["temperature"]))
            except Exception as e: rejected.append((line,str(e)))
    # median imputation per measurement column; if entire column absent, use 0
    for j in range(3,7):
        valid=[r[j] for r in cleaned if r[j] is not None]
        med=statistics.median(valid) if valid else 0.0
        cleaned=[r[:j]+(med,)+r[j+1:] if r[j] is None else r for r in cleaned]
    # remove duplicates on station/date/hour
    unique={}
    for r in cleaned: unique[(r[0],r[1],r[2])]=r
    return list(unique.values()), rejected

def create_db(rows, db_path):
    con=sqlite3.connect(db_path)
    con.execute("""CREATE TABLE IF NOT EXISTS readings(
      station TEXT NOT NULL, day TEXT NOT NULL, hour INTEGER NOT NULL,
      pm25 REAL, pm10 REAL, no REAL, temperature REAL,
      PRIMARY KEY(station,day,hour))""")
    con.executemany("INSERT OR REPLACE INTO readings VALUES(?,?,?,?,?,?,?)", rows)
    con.commit()
    return con

def daily_summary(con):
    return con.execute("""SELECT station,day,MIN(pm25),MAX(pm25),AVG(pm25),COUNT(pm25)
      FROM readings GROUP BY station,day ORDER BY station,day""").fetchall()
