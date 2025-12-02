from typing import TypedDict


class StorageConfig(TypedDict):
    output_dir: str
    sources_csv: str
    combined_csv: str


def load_storage_config() -> StorageConfig:
    config: StorageConfig = {
        "output_dir": "data/raw",
        "sources_csv": "sources.csv",
        "articles_csv": "articles_combined.csv",
    }

    return config
