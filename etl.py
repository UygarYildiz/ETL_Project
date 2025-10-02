import pandas as pd
from datas import db_engine

def extract_data(query: str) -> pd.DataFrame:
    """Extract data from the database using the provided SQL query."""
    query="""
     SELECT * FROM your_table"""
    with db_engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the data by cleaning and processing."""
    # Example transformation: Drop rows with any null values
    df_cleaned = df.dropna()
    df
    return df_cleaned