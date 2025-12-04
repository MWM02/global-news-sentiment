import pandas as pd
from typing import Tuple
from src.utils.logging_utils import setup_logger
from config.types import StorageConfig
from src.utils.file_utils import save_and_append_to_csv

logger = setup_logger("load_data", "load_data.log")


def load_data(
    clean_data: Tuple[
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
    ],
    storage_config: StorageConfig,
):
    try:
        sources, articles, authors, author_article, sources_articles = (
            clean_data
        )

        save_and_append_to_csv(
            sources,
            storage_config["clean_sources"],
        )
        save_and_append_to_csv(
            sources_articles,
            storage_config["clean_sources_articles"],
        )
        save_and_append_to_csv(
            articles,
            storage_config["clean_articles"],
        )
        save_and_append_to_csv(
            authors,
            storage_config["clean_authors"],
        )
        save_and_append_to_csv(
            author_article,
            storage_config["clean_author_article"],
        )
    except Exception as e:
        logger.error(f"Data load failed: {str(e)}")
        raise
