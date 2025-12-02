import os
import pandas as pd
from config.api_config import load_api_config
from config.storage_config import load_storage_config
from src.extract.extract_sources import extract_sources
from src.extract.extract_articles import extract_articles
from src.utils.file_utils import save_and_append_to_csv
from src.utils.logging_utils import setup_logger

logger = setup_logger("extract_data", "extract_data.log")


def extract_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    env = os.getenv("ENV", "unknown")
    try:
        api_config = load_api_config()
        storage_config = load_storage_config()

        if env == "test":
            sources_df = pd.read_csv("data/raw/sources.csv")
            articles_df = pd.read_csv("data/raw/articles_combined.csv")

        elif env == "dev":
            sources_df = extract_sources(api_config)
            save_and_append_to_csv(
                sources_df,
                storage_config["output_dir"],
                storage_config["sources_csv"],
            )
            sources_df = pd.read_csv("./data/raw/sources.csv")
            articles_df = extract_articles(sources_df, api_config)
            save_and_append_to_csv(
                articles_df,
                storage_config["output_dir"],
                storage_config["articles_csv"],
            )

        logger.info(
            f"Data extraction completed successfully - "
            f"Sources: {sources_df.shape}, Articles: {articles_df.shape}"
        )

        return sources_df, articles_df

    except Exception as e:
        logger.error(f"Data extraction failed: {str(e)}")
        raise
