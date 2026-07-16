import websocket

API_KEY = "6b1c069ede2add54461dfccd34fba3a81fb88843"

def on_message(ws, message):
    print("Mensaje recibido:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Conexión cerrada")

def on_open(ws):
    print("Conexión abierta a AISStream")

ws = websocket.WebSocketApp(
    f"wss://stream.aisstream.io/v1/stream?token={API_KEY}",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
ws.on_open = on_open
ws.run_forever()