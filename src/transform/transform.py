import pandas as pd
from typing import Tuple
from src.utils.logging_utils import setup_logger
from src.transform.clean_sources import clean_sources
from src.transform.clean_articles import clean_articles
from src.transform.normalise_articles import normalise_articles
from src.transform.filter_articles import filter_articles
from src.transform.merge_sources_articles import merge_sources_articles
from src.transform.enrich_sources_articles import enrich_sources_articles


logger = setup_logger("transform_data", "transform_data.log")


def transform_data(
    data: Tuple[pd.DataFrame, pd.DataFrame], max_article_age_days: int
) -> Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
]:
    try:
        logger.info("Starting data transformation process...")
        sources_df, articles_df = data
        logger.info("Cleaning source data...")
        cleaned_sources = clean_sources(sources_df)
        logger.info("Sources data successfully cleaned.")

        logger.info("Cleaning articles data...")
        cleaned_articles = clean_articles(articles_df)
        logger.info("Articles data successfully cleaned.")

        logger.info("Normalise articles data...")
        normalised_articles, authors, author_article = normalise_articles(
            cleaned_articles
        )
        logger.info("Articles data successfully normalised.")

        logger.info("Filtering articles...")
        filtered_articles = filter_articles(
            normalised_articles, max_article_age_days
        )
        logger.info("Articles data successfully filtered.")

        logger.info("Enriching data...")
        enriched_articles = enrich_sources_articles(filtered_articles)
        logger.info("Data enriched successfully.")

        logger.info("Merging sources and articles data...")
        merged_sources_articles = merge_sources_articles(
            cleaned_sources, enriched_articles
        )
        logger.info("Data merged successfully.")

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
