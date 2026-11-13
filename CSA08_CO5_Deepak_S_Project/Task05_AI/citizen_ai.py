from pathlib import Path
import re, collections
root=Path(__file__).resolve().parents[1]
POS={"good","clean","fast","helpful","improved"}
NEG={"bad","dirty","slow","rude","smoke","broken","worse","terrible","unhealthy","poor"}
NEGATORS={"not","never","no"}
def score(text):
    words=re.findall(r"[a-z']+",text.lower()); total=0
    for i,w in enumerate(words):
        value=1 if w in POS else -1 if w in NEG else 0
        if i and words[i-1] in NEGATORS: value=-value
        total+=value
    return total
def label(text):
    s=score(text); return "positive" if s>0 else "negative" if s<0 else "neutral"
def summarise(text, k=2):
    sentences=re.split(r"(?<=[.!?])\s+",text.strip())
    words=re.findall(r"[a-z']+",text.lower())
    stop={"the","is","and","a","to","of","in","near","was","are","on","for","with"}
    freq=collections.Counter(w for w in words if w not in stop)
    ranked=sorted(enumerate(sentences),key=lambda p:(-sum(freq[w] for w in re.findall(r"[a-z']+",p[1].lower())),p[0]))
    chosen={i for i,_ in ranked[:min(k,len(sentences))]}
    return " ".join(s for i,s in enumerate(sentences) if i in chosen)
complaints=(root/"citizen_complaints.txt").read_text(encoding="utf-8").splitlines()
print("Complaint count:",len(complaints))
for c in complaints[:8]: print(f"{label(c):8} | {c}")
print("Extractive summary:",summarise(" ".join(complaints[:5]),2))
# Simple human-labelled sample for agreement demonstration; labels are manually assigned in this script
human=["positive","negative","negative","positive","negative","positive","negative","negative","positive","negative"]
agree=sum(label(c)==h for c,h in zip(complaints[:10],human))
print(f"Manual review agreement: {agree}/10 = {agree*10}%")
def chatbot(question,con):
    m=re.search(r"pm\\s*2?\\.5.*?(?:in|at)\\s+([a-z ]+)",question.lower())
    if not m: return "Please ask: What is the PM2.5 in Adyar today?"
    station=m.group(1).strip().title()
    row=con.execute("SELECT AVG(pm25) FROM readings WHERE station=? AND day=(SELECT MAX(day) FROM readings)",(station,)).fetchone()
    return f"Latest available PM2.5 for {station}: {row[0]:.2f}" if row and row[0] is not None else "Station not found."
if __name__=="__main__":
 import sqlite3
 con=sqlite3.connect(root/"air_quality.sqlite")
 print(chatbot("What is the PM2.5 in Adyar today?",con)); con.close()
