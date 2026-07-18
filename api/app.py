# api/api.py
from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="db",
        database="marinetraffic",
        user="admin",
        password="admin"
    )

@app.get("/ships")
def get_ships():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT mmsi, latitude, longitude, speed, course FROM position_reports LIMIT 50;")
    rows = cur.fetchall()
    return [{"mmsi": r[0], "lat": r[1], "lon": r[2], "speed": r[3], "course": r[4]} for r in rows]

@app.get("/stats")
def get_stats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT mmsi), AVG(speed) FROM position_reports;")
    ships, avg_speed = cur.fetchone()
    return {"total_ships": ships, "avg_speed": avg_speed}
