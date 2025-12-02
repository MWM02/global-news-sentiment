from datetime import datetime, timedelta
from config.api_config import ApiConfig


def get_article_date_str(api_config: ApiConfig) -> str:
    days_before = api_config.get("days_before", 2)
    return (datetime.now() - timedelta(days=days_before)).strftime("%d-%m-%Y")
