from typing import TypedDict

PATH_FOR_RAW_DATA = "data/raw"
PATH_FOR_CLEAN_DATA = "data/processed"
SOURCES_FILE_NAME = "sources.csv"
ARTICLES_FILE_NAME = "articles.csv"


class StorageConfig(TypedDict):
    output_dir_for_raw_data: str
    output_dir_for_clean_data: str
    sources_file_name: str
    articles_file_name: str


def load_storage_config() -> StorageConfig:
    config: StorageConfig = {
        "output_dir_for_raw_data": PATH_FOR_RAW_DATA,
        "output_dir_for_clean_data": PATH_FOR_CLEAN_DATA,
        "sources_file_name": SOURCES_FILE_NAME,
        "articles_file_name": ARTICLES_FILE_NAME,
    }

    return config
