from pathlib import Path
import sys, sqlite3
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import load_and_clean,create_db,daily_summary
root=Path(__file__).resolve().parents[1]
rows,_=load_and_clean(root/"sample_air_quality.csv")
con=create_db(rows,root/"air_quality.sqlite")
# trend
data=con.execute("SELECT day,AVG(pm25) FROM readings WHERE station='Adyar' GROUP BY day ORDER BY day").fetchall()
plt.figure(figsize=(8,3.5)); plt.plot([x[0][-2:] for x in data],[x[1] for x in data],marker="o")
plt.title("Daily PM2.5 Trend - Adyar, October 2026"); plt.xlabel("Day of month"); plt.ylabel("PM2.5"); plt.tight_layout(); plt.savefig(root/"Task03_Analysis/adyar_trend.png"); plt.close()
# station comparison
data=con.execute("SELECT station,AVG(pm25) FROM readings GROUP BY station ORDER BY station").fetchall()
plt.figure(figsize=(9,4)); plt.bar([x[0] for x in data],[x[1] for x in data]); plt.xticks(rotation=55,ha="right")
plt.title("Average PM2.5 by Station"); plt.xlabel("Station"); plt.ylabel("Mean PM2.5"); plt.tight_layout(); plt.savefig(root/"Task03_Analysis/station_comparison.png"); plt.close()
# temperature relationship
data=con.execute("SELECT temperature,pm25 FROM readings").fetchall()
plt.figure(figsize=(6,4)); plt.scatter([x[0] for x in data],[x[1] for x in data],alpha=.35)
plt.title("Temperature vs PM2.5"); plt.xlabel("Temperature (°C)"); plt.ylabel("PM2.5"); plt.tight_layout(); plt.savefig(root/"Task03_Analysis/temp_scatter.png"); plt.close()
# hour distribution
data=con.execute("SELECT hour,AVG(pm25) FROM readings GROUP BY hour ORDER BY hour").fetchall()
plt.figure(figsize=(6,3.5)); plt.bar([x[0] for x in data],[x[1] for x in data])
plt.title("Average PM2.5 by Reporting Hour"); plt.xlabel("Hour"); plt.ylabel("Mean PM2.5"); plt.tight_layout(); plt.savefig(root/"Task03_Analysis/hourly_bar.png"); plt.close()
print("Charts saved: adyar_trend.png, station_comparison.png, temp_scatter.png, hourly_bar.png")
print("Daily summary sample:")
for r in daily_summary(con)[:3]: print(r)
con.close()
