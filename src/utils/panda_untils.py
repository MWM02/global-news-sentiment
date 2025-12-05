import pandas as pd
from typing import List


def drop_duplicate_rows(
    df: pd.DataFrame, check_cols: List[str]
) -> pd.DataFrame:
    return df.drop_duplicates(subset=check_cols)


def remove_missing_values(
    df: pd.DataFrame, check_columns: List[str]
) -> pd.DataFrame:
    df = df.dropna(subset=check_columns)
    return df


def remove_unneeded_columns(
    df: pd.DataFrame, columns_to_drop: List[str]
) -> pd.DataFrame:
    df = df.drop(columns=columns_to_drop)
    return df


def filter_by_date(
    df: pd.DataFrame, date_column: str, threshold: pd.Timestamp
) -> pd.DataFrame:
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    return df[df[date_column] >= threshold]


def standardise_date(date_str: str) -> pd.Timestamp:
    if pd.isna(date_str) or date_str == "":
        return pd.NaT

    return pd.to_datetime(date_str, errors="coerce", utc=True)
