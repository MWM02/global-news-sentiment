import logging
import requests
import timeit
import pandas as pd
from config.api_config import ApiConfig
from src.utils.api_utils import handle_api_response
from src.utils.logging_utils import setup_logger, log_extract_success

logger = setup_logger(__name__, "extract_sources.log", level=logging.DEBUG)
EXPECTED_IMPORT_RATE = 0.001
TYPE = "Sources from NewsAPI"


def extract_sources(api_config: ApiConfig) -> pd.DataFrame:
    try:
        start_time = timeit.default_timer()
        sources_df = extract_sources_execution(api_config)
        duration = timeit.default_timer() - start_time

        if sources_df.empty:
            logger.warning("No sources returned from API.")
            return pd.DataFrame()

        log_extract_success(
            logger, TYPE, sources_df.shape, duration, EXPECTED_IMPORT_RATE
        )
        return sources_df
    except Exception as e:
        logger.error(f"Failed to extract sources: {e}")
        raise Exception(f"Failed to extract sources: {e}")


def extract_sources_execution(api_config: ApiConfig) -> pd.DataFrame:
    api_key = api_config["api_key"]
    language = api_config["language"]

    base_url = api_config["base_url"]
    endpoint = api_config["sources_endpoint"]
    url = f"{base_url}{endpoint}"

    params = {"apiKey": api_key, "language": language}

    response = requests.get(url, params=params, timeout=10)
    data = handle_api_response(response)

    sources_list = data.get("sources", [])
    return pd.DataFrame(sources_list)
