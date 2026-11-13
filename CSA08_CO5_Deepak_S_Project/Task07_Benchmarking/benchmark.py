from pathlib import Path
import sys,csv,sqlite3,time,statistics,cProfile,pstats,io,random
root=Path(__file__).resolve().parents[1]
def make_data(stations):
 p=root/"Task07_Benchmarking"/f"generated_{stations}.csv"
 with p.open("w",newline="",encoding="utf-8") as f:
  w=csv.writer(f); w.writerow(["station","day","pm25"])
  for s in range(stations):
   for d in range(365):
    for h in range(24):
     w.writerow([f"S{s:03}",f"2026-{d//30+1:02}-{d%30+1:02}",round(random.uniform(5,150),2)])
 return p
def loops(path):
 d={}
 with open(path,newline="",encoding="utf-8") as f:
  for r in csv.DictReader(f):
   k=(r["station"],r["day"]); a=d.setdefault(k,[0.0,0]); a[0]+=float(r["pm25"]); a[1]+=1
 return {k:v[0]/v[1] for k,v in d.items()}
def pandas_method(path):
 import pandas as pd
 df=pd.read_csv(path); return df.groupby(["station","day"])["pm25"].mean().to_dict()
def sql_method(path):
 con=sqlite3.connect(":memory:")
 con.execute("CREATE TABLE r(station TEXT,day TEXT,pm25 REAL)")
 with open(path,newline="",encoding="utf-8") as f:
  data=list(csv.DictReader(f))
 con.executemany("INSERT INTO r VALUES(?,?,?)",[(x["station"],x["day"],float(x["pm25"])) for x in data])
 out=con.execute("SELECT station,day,AVG(pm25) FROM r GROUP BY station,day").fetchall()
 con.close(); return {(a,b):c for a,b,c in out}
for n in (1,12,120):
 p=make_data(n); print(f"Stations={n}, readings={n*8760}")
 results={}
 for name,fn in [("loops",loops),("pandas",pandas_method),("sql",sql_method)]:
  t=time.perf_counter(); out=fn(p); elapsed=time.perf_counter()-t
  results[name]=out; print(f"  {name:7} {elapsed:.4f}s groups={len(out)}")
 print("  outputs agree:",len(results["loops"])==len(results["pandas"])==len(results["sql"]) and all(abs(results["loops"][k]-results["sql"][k])<1e-8 for k in results["loops"]))
p=make_data(1); pr=cProfile.Profile(); pr.enable(); loops(p); pr.disable()
s=io.StringIO(); pstats.Stats(pr,stream=s).sort_stats("cumulative").print_stats(8)
(root/"Task07_Benchmarking"/"profile.txt").write_text(s.getvalue(),encoding="utf-8")
print("Profile saved to profile.txt")
