from datetime import datetime, timedelta


def get_date_str(days_back: int) -> str:
    return (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
