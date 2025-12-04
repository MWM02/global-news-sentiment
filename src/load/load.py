import pandas as pd
from typing import Tuple
from src.utils.logging_utils import setup_logger
from config.storage_config import load_storage_config
from src.utils.file_utils import save_and_append_to_csv


logger = setup_logger("load_data", "load_data.log")


def load_data(
    clean_data: Tuple[
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
    ],
):
    try:
        storage_config = load_storage_config()
        sources, articles, authors, author_article, sources_articles = (
            clean_data
        )
        save_and_append_to_csv(
            sources,
            storage_config["output_dir_for_clean_data"],
            "sources.csv",
        )
        save_and_append_to_csv(
            sources_articles,
            storage_config["output_dir_for_clean_data"],
            "sources_articles.csv",
        )
        save_and_append_to_csv(
            articles,
            storage_config["output_dir_for_clean_data"],
            "articles.csv",
        )
        save_and_append_to_csv(
            authors, storage_config["output_dir_for_clean_data"], "authors.csv"
        )
        save_and_append_to_csv(
            author_article,
            storage_config["output_dir_for_clean_data"],
            "author_article.csv",
        )
    except Exception as e:
        logger.error(f"Data load failed: {str(e)}")
        raise
