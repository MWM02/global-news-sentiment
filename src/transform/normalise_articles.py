import pandas as pd
from typing import Tuple


def normalise_articles(
    articles: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    normalised_articles = articles.drop(columns=["author(s)"]).reset_index(
        drop=True
    )
    normalised_articles.insert(0, "id", range(1, len(articles) + 1))

    all_authors = articles["author(s)"].explode().dropna().unique()
    authors = pd.DataFrame({"author": all_authors})
    authors = authors.reset_index(drop=True)
    authors.insert(0, "id", range(1, len(authors) + 1))

    exploded_articles = articles.copy()
    exploded_articles.insert(0, "article_id", range(1, len(articles) + 1))
    exploded_articles = exploded_articles.explode("author(s)")
    author_articles = exploded_articles[["article_id", "author(s)"]].rename(
        columns={"author(s)": "author"}
    )
    author_article = author_articles.merge(authors, on="author", how="inner")
    author_article = author_article[["article_id", "id"]].rename(
        columns={"id": "author_id"}
    )

    return (normalised_articles, authors, author_article)
