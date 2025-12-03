import os
from typing import TypedDict


class ETLConfig(TypedDict):
    max_article_age_days: int
    days_back: int
    cycle_num: int
    cycle_interval_hours: float


def load_etl_config() -> ETLConfig:
    config: ETLConfig = {
        "max_article_age_days": int(os.getenv("MAX_ARTICLE_AGE_DAYS", 7)),
        "days_back": int(os.getenv("DAYS_BACK", 2)),
        "cycle_num": int(os.getenv("CYCLE_NUMBER")),
        "cycle_interval_hours": int(
            os.getenv(
                "CYCLE_INTERVAL_HOURS",
            )
        ),
    }

    return config
