import pandas as pd
from typing import Tuple
from config.etl_config import load_etl_config
from config.storage_config import load_storage_config
from src.utils.file_utils import save_and_append_to_csv
from src.utils.logging_utils import setup_logger
from src.transform.clean_sources import clean_sources
from src.transform.clean_articles import clean_articles
from src.transform.normalise_articles import normalise_articles
from src.transform.filter_articles import filter_articles
from src.transform.merge_sources_articles import merge_sources_articles
from src.transform.enrich_sources_articles import enrich_sources_articles


logger = setup_logger("transform_data", "transform_data.log")


def transform_data(
    data: Tuple[pd.DataFrame, pd.DataFrame],
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        etl_config = load_etl_config()
        storage_config = load_storage_config()

        logger.info("Starting data transformation process...")

        logger.info("Cleaning source data...")
        cleaned_sources = clean_sources(data[0])
        logger.info("Sources data successfully cleaned.")

        logger.info("Cleaning articles data...")
        cleaned_articles = clean_articles(data[1])
        logger.info("Articles data successfully cleaned.")

        logger.info("Normalise articles data...")
        normalised_articles, authors, author_article = normalise_articles(
            cleaned_articles
        )
        logger.info("Articles data successfully normalised.")

        logger.info("Filtering articles...")
        filtered_articles = filter_articles(normalised_articles, etl_config)
        logger.info("Articles data successfully filtered.")

        logger.info("Enriching data...")
        enriched_articles = enrich_sources_articles(filtered_articles)
        logger.info("Data enriched succesfully.")

        logger.info("Merging sources and articles data...")
        merged_sources_articles = merge_sources_articles(
            cleaned_sources, enriched_articles
        )
        logger.info("Data merged successfully.")
        save_and_append_to_csv(
            cleaned_sources,
            storage_config["output_dir_for_clean_data"],
            "sources.csv",
        )
        save_and_append_to_csv(
            merged_sources_articles,
            storage_config["output_dir_for_clean_data"],
            "sources_articles.csv",
        )
        save_and_append_to_csv(
            filtered_articles,
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
        logger.info("Data transformation complete.")

        return (
            cleaned_sources,
            filtered_articles,
            authors,
            author_article,
            merged_sources_articles,
        )

    except Exception as e:
        logger.error(f"Data transformation failed: {str(e)}")
        raise
