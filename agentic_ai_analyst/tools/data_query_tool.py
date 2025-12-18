import pandas as pd
from pathlib import Path 
Data_Path= Path("data")

def load_table(table_name: str) -> pd.DataFrame:
    file_path = Data_Path / f"{table_name}.csv"
    if not file_path.exists():
        raise ValueError(f"Table {table_name} does not exist")
    return pd.read_csv(file_path)

def query_table(table_name: str,filters: dict=None) -> pd.DataFrame:
    df=load_table(table_name)

    if filters:
        for column,value in filters.items():
            df =df[df[column]==value]

    return df










