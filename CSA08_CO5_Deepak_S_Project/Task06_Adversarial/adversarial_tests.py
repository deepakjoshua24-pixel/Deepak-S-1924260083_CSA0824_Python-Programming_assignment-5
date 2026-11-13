from pathlib import Path
import sys,sqlite3,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import load_and_clean
root=Path(__file__).resolve().parents[1]
tests={
"missing_column":"station,date,pm25\\nAdyar,2026-10-01,20\\n",
"wrong_delimiter":"station;date;hour;pm25;pm10;no;temperature\\nAdyar;2026-10-01;0;20;30;5;30\\n",
"empty":""
}
for name,data in tests.items():
 p=root/"Task06_Adversarial"/f"{name}.csv"; p.write_text(data,encoding="utf-8")
 try: print(name,load_and_clean(p)[0][:1])
 except Exception as e: print(name,"handled:",type(e).__name__,str(e))
con=sqlite3.connect(":memory:"); con.execute("CREATE TABLE aq(station TEXT,pm25 REAL)")
con.executemany("INSERT INTO aq VALUES(?,?)",[("Adyar",48),("Guindy",95)])
payload="Adyar' OR '1'='1"
unsafe="SELECT AVG(pm25) FROM aq WHERE station='"+payload+"'"
safe=con.execute("SELECT AVG(pm25) FROM aq WHERE station=?",(payload,)).fetchone()[0]
print("Unsafe concatenated query:",con.execute(unsafe).fetchone()[0])
print("Safe parameterised query:",safe)
con.close()
