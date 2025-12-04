import os
from config.types import ETLConfig


def load_etl_config() -> ETLConfig:
    return {
        "max_article_age_days": int(os.getenv("MAX_ARTICLE_AGE_DAYS", 7)),
        "days_back": int(os.getenv("DAYS_BACK", 2)),
        "cycle_num": int(os.getenv("CYCLE_NUMBER", 1)),
        "cycle_interval_hours": float(os.getenv("CYCLE_INTERVAL_HOURS", 24)),
    }
