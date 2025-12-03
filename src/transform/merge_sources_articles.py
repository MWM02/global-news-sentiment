import pandas as pd
from src.utils.panda_untils import remove_unneeded_columns


def merge_sources_articles(
    sources: pd.DataFrame, articles: pd.DataFrame
) -> pd.DataFrame:
    sources = sources.rename(
        columns={
            "id": "source_id",
            "description": "source_description",
            "name": "source_name",
        }
    )
    sources_articles = merge_on_source_id(articles, sources)
    sources_articles = remove_unneeded_columns(sources_articles, ["source_id"])
    return sources_articles


def merge_on_source_id(
    articles: pd.DataFrame, sources: pd.DataFrame
) -> pd.DataFrame:
    return articles.merge(
        sources,
        on="source_id",
        how="left",
    )
