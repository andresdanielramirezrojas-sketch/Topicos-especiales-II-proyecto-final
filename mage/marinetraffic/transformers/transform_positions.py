import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Si no llegaron datos
    if df.empty:
        return df

    # Eliminar registros sin coordenadas
    df = df.dropna(subset=["latitude", "longitude"])

    # Eliminar registros sin MMSI
    df = df.dropna(subset=["mmsi"])

    # Convertir tipos
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df["speed"] = (
        pd.to_numeric(df["speed"], errors="coerce")
        .fillna(0)
    )

    df["course"] = (
        pd.to_numeric(df["course"], errors="coerce")
        .fillna(0)
    )

    # Eliminar posibles registros inválidos después de convertir
    df = df.dropna(subset=["latitude", "longitude"])

    df["timestamp"] = (
        df["timestamp"]
        .str.replace(" UTC", "", regex=False)
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="coerce"
    )

    df["timestamp"] = df["timestamp"].dt.tz_localize(None)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
