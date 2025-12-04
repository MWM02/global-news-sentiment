import pandas as pd
from src.utils.date_utils import get_date_str
from src.utils.panda_untils import filter_by_date


def filter_articles(
    articles: pd.DataFrame, max_article_age_days: int
) -> pd.DataFrame:
    threshold_date = get_threshold_date(max_article_age_days)
    articles = filter_by_date(articles, "published_at", threshold_date)
    return articles


def get_threshold_date(max_age_days: int) -> pd.Timestamp:
    date_str = get_date_str(max_age_days)
    return pd.to_datetime(date_str, utc=True)
