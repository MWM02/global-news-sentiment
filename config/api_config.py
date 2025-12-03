import os
from typing import TypedDict

DEFAULT_LANGUAGE = "en"
DEFAULT_SORT_BY = "popularity"
BASE_URL = "https://newsapi.org/v2"
SOURCES_ENDPOINT = "/top-headlines/sources"
ARTICLES_ENDPOINT = "/everything"


class ApiConfigError(Exception):
    """Custom exception for API configuration errors."""

    pass


class ApiConfig(TypedDict):
    api_key: str
    language: str
    sort_by: str
    request_limit: int
    interval_seconds: int
    base_url: str
    sources_endpoint: str
    articles_endpoint: str


def load_api_config() -> ApiConfig:
    api_key = os.getenv("NEWSAPI_KEY", "error")

    if api_key == "error":
        raise ApiConfigError("Configuration error: NEWSAPI_KEY is not set")

    config: ApiConfig = {
        "api_key": api_key,
        "language": DEFAULT_LANGUAGE,
        "sort_by": DEFAULT_SORT_BY,
        "request_limit": int(os.getenv("NEWSAPI_REQUEST_LIMIT", 95)),
        "interval_seconds": int(
            os.getenv("NEWSAPI_REQUEST_INTERVAL_SECONDS", 15)
        ),
        "base_url": BASE_URL,
        "sources_endpoint": SOURCES_ENDPOINT,
        "articles_endpoint": ARTICLES_ENDPOINT,
    }

    return config
