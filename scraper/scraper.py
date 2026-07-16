import os
import psycopg2
import asyncio
import websockets
import json
import time
from datetime import datetime, timezone

API_KEY = os.getenv("API_KEY")

# Función con reintentos para conectar a Postgres
def get_conn(max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            return psycopg2.connect(
                host="db",
                database="marinetraffic",
                user="admin",
                password="admin"
            )
        except psycopg2.OperationalError:
            print(f"⚠️ Postgres no está listo (intento {attempt+1}/{max_retries}), reintentando en {delay}s...")
            time.sleep(delay)
    raise Exception("❌ No se pudo conectar a Postgres después de varios intentos")

async def connect_ais_stream():
    uri = "wss://stream.aisstream.io/v0/stream"

    async with websockets.connect(uri) as websocket:
        # BoundingBox para la entrada Caribe del Canal de Panamá (Colón/Cristóbal)
        # Coordenadas aproximadas: lat 9.3 a 9.5, lon -79.95 a -79.7
        subscribe_message = {
            "APIKey": API_KEY,
            "BoundingBoxes": [[[8.8, -80.2], [9.8, -79.3]]],
            "FilterMessageTypes": ["PositionReport"]
        }
        await websocket.send(json.dumps(subscribe_message))
        print("🌐 Conectado a AISStream (entrada Caribe del Canal de Panamá). Esperando datos...")

        async for message_json in websocket:
            data = json.loads(message_json)
            if data.get("MessageType") == "PositionReport":
                ais_message = data["Message"]["PositionReport"]
                mmsi = ais_message.get("UserID")
                lat = ais_message.get("Latitude")
                lon = ais_message.get("Longitude")
                speed = ais_message.get("Sog", 0)
                course = ais_message.get("Cog", 0)

                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO position_reports (mmsi, latitude, longitude, speed, course, report_time)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                    """, (mmsi, lat, lon, speed, course))
                    conn.commit()
                    cur.close()
                    conn.close()
                    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{ts}] ✅ Insertado: {mmsi} en {lat}, {lon}")
                except Exception as e:
                    print("❌ Error insertando:", e)

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(connect_ais_stream())
        except Exception as e:
            print("❌ Error de conexión:", e)
            time.sleep(5)
