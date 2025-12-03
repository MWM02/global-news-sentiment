import os
import pandas as pd
from config.api_config import load_api_config
from config.storage_config import load_storage_config
from config.etl_config import load_etl_config
from src.extract.extract_sources import extract_sources
from src.extract.extract_articles import extract_articles
from src.utils.file_utils import save_and_append_to_csv
from src.utils.logging_utils import setup_logger

logger = setup_logger("extract_data", "extract_data.log")


def extract_data(env: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        storage_config = load_storage_config()

        if env == "test":
            raw_sources_file_path = os.path.join(
                storage_config["output_dir_for_raw_data"],
                storage_config["sources_file_name"],
            )
            raw_articles_file_path = os.path.join(
                storage_config["output_dir_for_raw_data"],
                storage_config["articles_file_name"],
            )

            try:
                sources_df = pd.read_csv(raw_sources_file_path)
                articles_df = pd.read_csv(raw_articles_file_path)

            except FileNotFoundError as e:
                logger.exception(f"File not found: {e.filename}")
                raise

            logger.info("Data extraction skipped... Using local data.")

        elif env == "dev":
            api_config = load_api_config()
            etl_config = load_etl_config()
            sources_df = extract_sources(api_config)
            save_and_append_to_csv(
                sources_df,
                storage_config["output_dir_for_raw_data"],
                storage_config["sources_file_name"],
            )

            articles_df = extract_articles(sources_df, api_config, etl_config)
            save_and_append_to_csv(
                articles_df,
                storage_config["output_dir_for_raw_data"],
                storage_config["articles_file_name"],
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
