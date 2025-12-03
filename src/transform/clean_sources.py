import pandas as pd
from src.utils.panda_untils import (
    drop_duplicate_rows,
    remove_unneeded_columns,
)


def clean_sources(sources: pd.DataFrame) -> pd.DataFrame:
    sources = drop_duplicate_rows(sources, ["id"])
    sources = remove_unneeded_columns(sources, ["url"])
    return sources
