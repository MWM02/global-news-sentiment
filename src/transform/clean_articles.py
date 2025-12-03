import pandas as pd
import re
from src.utils.panda_untils import (
    drop_duplicate_rows,
    remove_missing_values,
    remove_unneeded_columns,
    standardise_date,
)


def clean_articles(articles: pd.DataFrame) -> pd.DataFrame:
    articles = drop_duplicate_rows(articles, ["url"])
    articles = remove_missing_values(articles, ["title", "description"])
    articles["published_at"] = articles["publishedAt"].apply(standardise_date)
    articles = clean_authors(articles)
    articles = remove_unneeded_columns(
        articles,
        [
            "url",
            "urlToImage",
            "publishedAt",
            "content",
            "author",
            "source_name",
        ],
    )
    return articles


def clean_authors(articles: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the 'author' column by:
    - Spliting by multiple separators
    - Removing emails
    - Keep only items with exactly 2 words
    - Removing items matching source names
    - Fill empty author rows with source_name
    """
    source_set = set(articles["source_name"].str.lower())

    separators = [",", " and ", "-", "|"]
    sep_regex = "|".join(map(re.escape, separators))

    def clean_author_row(author, source):
        if not author or pd.isna(author):
            return source.title() if pd.notna(source) else None

        author = re.sub(r"\S+@\S+\.\S+", "", str(author))
        items = [
            item.strip()
            for item in re.split(sep_regex, author)
            if item.strip()
        ]

        cleaned_authors = []
        for item in items:
            if len(item.split()) != 2:
                continue
            if item.lower() in source_set:
                continue

            cleaned_authors.append(item.title())

        if not cleaned_authors and pd.notna(source):
            cleaned_authors.append(source)

        return cleaned_authors

    articles["author(s)"] = articles.apply(
        lambda row: clean_author_row(row["author"], row["source_name"]),
        axis=1,
    )

    return articles
