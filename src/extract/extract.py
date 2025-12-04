import os
import pandas as pd
from typing import Tuple
from config.types import ETLPipelineConfigs
from src.extract.extract_sources import extract_sources
from src.extract.extract_articles import extract_articles
from src.utils.file_utils import save_and_append_to_csv
from src.utils.logging_utils import setup_logger

logger = setup_logger("extract_data", "extract_data.log")


def extract_data(
    env: str, configs: ETLPipelineConfigs
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        storage_config = configs["storage"]

        if env == "test":
            raw_sources_file_path = storage_config["raw_sources"]
            raw_articles_file_path = storage_config["raw_articles"]

            try:
                sources_df = pd.read_csv(raw_sources_file_path)
                articles_df = pd.read_csv(raw_articles_file_path)
            except FileNotFoundError as e:
                logger.exception(f"File not found: {e.filename}")
                raise

            logger.info("Data extraction skipped... Using local data.")

        elif env == "dev":
            api_config = configs["api"]
            etl_config = configs["etl"]

            sources_df = extract_sources(api_config)
            articles_df = extract_articles(sources_df, api_config, etl_config)

            if sources_df.empty:
                logger.error("API returned no sources. Stopping ETL...")
                raise ValueError("Empty sources dataframe returned from API.")

            if articles_df.empty:
                logger.error("API returned no articles. Stopping ETL...")
                raise ValueError("Empty articles dataframe returned from API.")

            save_and_append_to_csv(
                sources_df, storage_config["raw_dir"], "sources.csv"
            )
            save_and_append_to_csv(
                articles_df, storage_config["raw_dir"], "articles.csv"
            )

            logger.info(
                f"Data extraction completed successfully - "
                f"Sources: {sources_df.shape}, Articles: {articles_df.shape}"
            )

        else:
            logger.error(f"Unknown environment: {env}")
            raise

        return sources_df, articles_df

    except Exception as e:
        logger.error(f"Data extraction failed: {str(e)}")
        raise
