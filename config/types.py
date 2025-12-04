from typing import TypedDict


class ETLConfig(TypedDict):
    max_article_age_days: int
    days_back: int
    cycle_num: int
    cycle_interval_hours: float


class ApiConfig(TypedDict):
    api_key: str
    language: str
    sort_by: str
    request_limit: int
    interval_seconds: int
    base_url: str
    sources_endpoint: str
    articles_endpoint: str


class StorageConfig(TypedDict):
    raw_dir: str
    clean_dir: str
    raw_sources: str
    raw_articles: str
    clean_sources: str
    clean_articles: str
    clean_authors: str
    clean_author_article: str
    clean_sources_articles: str


class ETLPipelineConfigs(TypedDict):
    etl: ETLConfig
    api: ApiConfig
    storage: StorageConfig
