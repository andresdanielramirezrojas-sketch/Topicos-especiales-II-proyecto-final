import json
import websocket
import pandas as pd
import time

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

AISSTREAM_API_KEY = "715ac72120c93dffc9e09022e49e16ea14921b4d"


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    ships = []

    url = "wss://stream.aisstream.io/v0/stream"

    def on_message(ws, message):
        print(message)

        data = json.loads(message)

        if "Message" not in data:
            return

        message = data["Message"]

        if "PositionReport" not in message:
            return

        report = message["PositionReport"]
        metadata = data.get("MetaData", {})

        ships.append({
            "mmsi": metadata.get("MMSI"),
            "latitude": report.get("Latitude"),
            "longitude": report.get("Longitude"),
            "speed": report.get("Sog"),
            "course": report.get("Cog"),
            "timestamp": metadata.get("time_utc")
        })

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message
    )

    def on_error(ws, error):
        print("ERROR:", error)

    def on_close(ws, code, reason):
        print("CLOSE:", code, reason)

    def on_open(ws):
        print("Conectando a AISSTREAM")

        subscription = {
            "APIKey": AISSTREAM_API_KEY,
        "BoundingBoxes": [
            [[7.0, -83.0], [9.7, -77.0]],   # Atlántico (Colón)
        ],
            "FilterMessageTypes": ["PositionReport"]
        }

        ws.send(json.dumps(subscription))

    ws.on_open = on_open

    import threading

    thread = threading.Thread(target=ws.run_forever)

    thread.start()

    time.sleep(240)

    ws.close()

    thread.join()

    df = pd.DataFrame(ships)

    if not df.empty:
        print(f"Barcos recibidos: {len(df)}")
        print(df.head())
    else:
        print("No se recibieron barcos en este intervalo.")

    print(df.head())

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'