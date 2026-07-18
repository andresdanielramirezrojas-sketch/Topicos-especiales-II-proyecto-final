import psycopg2
from psycopg2.extras import execute_values
import pandas as pd


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(df, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    if df.empty:
        print("No hay datos para guardar.")
        return

    conn = psycopg2.connect(
        host="db",
        database="marinetraffic",
        user="admin",
        password="admin"
    )

    cur = conn.cursor()

    df["timestamp"] = (
        pd.to_datetime(
            df["timestamp"]
                .astype(str)
                .str.replace(" UTC", "", regex=False)
                .str.replace(r"(\.\d{6})\d+", r"\1", regex=True),
            utc=True,
            errors="coerce"
        )
        .dt.tz_localize(None)
    )

    # Guardar información del barco
    for _, row in df.iterrows():

        cur.execute("""
            INSERT INTO ships(
                mmsi,
                name,
                imo,
                ship_type,
                flag
            )
            VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT (mmsi)
            DO NOTHING;
        """,
        (
            row["mmsi"],
            None,
            None,
            None,
            None
        ))

    # Guardar posiciones
    values = []

    for _, row in df.iterrows():

        values.append(
            (
                row["mmsi"],
                row["latitude"],
                row["longitude"],
                row["speed"],
                row["course"],
                row["timestamp"]
            )
        )

    execute_values(
        cur,
        """
        INSERT INTO position_reports(

            mmsi,
            latitude,
            longitude,
            speed,
            course,
            report_time

        )
        VALUES %s;
        """,
        values
    )

    conn.commit()

    cur.close()
    conn.close()

    print(f"Guardados {len(df)} registros.")


