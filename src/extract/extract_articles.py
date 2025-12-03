import logging
import requests
import timeit
import time
import pandas as pd
from config.api_config import ApiConfig
from config.etl_config import ETLConfig
from src.utils.api_utils import handle_api_response
from src.utils.date_utils import get_date_str
from src.utils.logging_utils import setup_logger, log_extract_success

EXPECTED_IMPORT_RATE = 1000
TYPE = "Articles from NewsAPI"

logger = setup_logger(__name__, "extract_articles.log", level=logging.DEBUG)


def extract_articles(
    sources_df: pd.DataFrame, api_config: ApiConfig, etl_config: ETLConfig
) -> pd.DataFrame:

    start_time = timeit.default_timer()
    if sources_df.empty or "id" not in sources_df.columns:
        logger.warning(
            "No sources provided. Returning empty articles DataFrame."
        )
        duration = timeit.default_timer() - start_time
        logger.info(f"Article extraction finished in {duration} seconds")
        return pd.DataFrame()

    date_str = get_date_str(etl_config["days_back"])
    request_limit = api_config["request_limit"]
    interval_seconds = api_config["interval_seconds"]

    source_ids = sources_df["id"].tolist()
    all_articles: list[pd.DataFrame] = []
    request_count = 0

    logger.info(
        f"Starting article extraction for {len(source_ids)} "
        f"sources from {date_str} "
        f"(request_limit={request_limit}, interval_seconds={interval_seconds})"
    )

    for source_id in source_ids:
        request_count += 1

        if request_count > request_limit:
            logger.warning(
                f"Request limit reached after {request_count - 1} requests."
            )
            break

        try:
            articles = extract_articles_for_source_execution(
                api_config, source_id, date_str
            )

            if not articles.empty:
                all_articles.append(articles)
                logger.debug(
                    f"Fetched {len(articles)} articles for source {source_id}"
                )
            else:
                logger.info(f"No articles returned for source {source_id}")

        except Exception as e:
            logger.error(
                f"Failed to fetch articles for source {source_id}: {e}"
            )
            return pd.DataFrame()

        if request_count < request_limit and request_count < len(source_ids):
            time.sleep(interval_seconds)

    if not all_articles:
        logger.warning("No articles extracted from any source.")
        return pd.DataFrame()

    combined_articles_df = pd.concat(all_articles, ignore_index=True)
    duration = timeit.default_timer() - start_time

    log_extract_success(
        logger,
        TYPE,
        combined_articles_df.shape,
        duration,
        expected_rate=EXPECTED_IMPORT_RATE,
    )

    return combined_articles_df


def extract_articles_for_source_execution(
    api_config: ApiConfig, source_id: str, date_str: str
) -> pd.DataFrame:
    api_key = api_config["api_key"]
    language = api_config["language"]
    sort_by = api_config["sort_by"]

    base_url = api_config["base_url"]
    endpoint_url = api_config["articles_endpoint"]
    url = f"{base_url}{endpoint_url}"

    params = {
        "apiKey": api_key,
        "language": language,
        "sortBy": sort_by,
        "from": date_str,
        "to": date_str,
        "sources": source_id,
    }

    response = requests.get(url, params=params, timeout=10)
    data = handle_api_response(response)
    articles_list = data.get("articles", [])

    if not articles_list:
        return pd.DataFrame()

    articles_df = pd.json_normalize(articles_list, sep="_")
    return articles_df
