import os
from config.types import StorageConfig

BASE_DIR = "data"
RAW_DIR = os.path.join(BASE_DIR, "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "processed")


def load_storage_config() -> StorageConfig:
    return {
        "raw_dir": RAW_DIR,
        "clean_dir": CLEAN_DIR,
        "raw_sources": os.path.join(RAW_DIR, "sources.csv"),
        "raw_articles": os.path.join(RAW_DIR, "articles.csv"),
        "clean_sources": os.path.join(CLEAN_DIR, "sources.csv"),
        "clean_articles": os.path.join(CLEAN_DIR, "articles.csv"),
        "clean_authors": os.path.join(CLEAN_DIR, "authors.csv"),
        "clean_author_article": os.path.join(CLEAN_DIR, "author_article.csv"),
        "clean_sources_articles": os.path.join(
            CLEAN_DIR, "sources_articles.csv"
        ),
    }
