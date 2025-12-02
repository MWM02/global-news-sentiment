import os
from typing import TypedDict


class ApiConfigError(Exception):
    """Custom exception for API configuration errors."""

    pass


class ApiConfig(TypedDict):
    api_key: str
    language: str
    sort_by: str
    request_limit: int
    interval_seconds: int
    days_before: int
    base_url: str
    sources_endpoint: str
    articles_endpoint: str


def load_api_config() -> ApiConfig:
    api_key = os.getenv("NEWSAPI_KEY", "error")

    if api_key == "error":
        raise ApiConfigError("Configuration error: NEWSAPI_KEY is not set")

    config: ApiConfig = {
        "api_key": api_key,
        "language": "en",
        "sort_by": "popularity",
        "request_limit": 95,
        "interval_seconds": 15,
        "days_before": 2,
        "base_url": "https://newsapi.org/v2",
        "sources_endpoint": "/top-headlines/sources",
        "articles_endpoint": "/everything",
    }

    return config
