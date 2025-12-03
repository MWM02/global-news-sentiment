import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


def enrich_sources_articles(articles: pd.DataFrame):
    articles = add_sentiment_scores(articles, "title")
    articles = add_sentiment_scores(articles, "description")
    return articles


def add_sentiment_scores(df: pd.DataFrame, df_col: str) -> pd.DataFrame:
    scores = df[df_col].apply(sia.polarity_scores)
    scores_df = scores.apply(pd.Series)
    scores_df = scores_df.rename(
        columns={
            "neg": f"sentiment_negative_by_{df_col}",
            "neu": f"sentiment_neutral_by_{df_col}",
            "pos": f"sentiment_positive_by_{df_col}",
            "compound": f"overall_sentiment_by_{df_col}",
        }
    )

    scores_df[f"sentiment_label_by_{df_col}"] = scores_df[
        f"overall_sentiment_by_{df_col}"
    ].apply(label_sentiment)

    df = pd.concat([df, scores_df], axis=1)
    return df


def label_sentiment(compound_score: float) -> str:
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"
