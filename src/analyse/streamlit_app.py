import streamlit as st
import pandas as pd
import plotly.express as px


def load_data():
    authors = pd.read_csv("data/processed/authors.csv")
    author_article = pd.read_csv("data/processed/author_article.csv")
    sources_articles = pd.read_csv("data/processed/sources_articles.csv")

    sources_articles["published_at"] = pd.to_datetime(
        sources_articles["published_at"], errors="coerce"
    )

    return authors, author_article, sources_articles


authors, author_article, sources_articles = load_data()

st.title("Global News Sentiment")

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Number of Articles", len(sources_articles))

with col2:
    st.metric("Number of Sources", sources_articles["source_name"].nunique())

with col3:
    st.metric(
        "Avg Sentiment For Title",
        round(sources_articles["overall_sentiment_by_title"].mean(), 3),
    )

with col4:
    st.metric(
        "Avg Sentiment For Description",
        round(sources_articles["overall_sentiment_by_description"].mean(), 3),
    )


# Sentiment Distribution (Pie Charts)
st.subheader("Sentiment Distribution")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(
        sources_articles,
        names="sentiment_label_by_title",
        title="Sentiment Labels For Titles",
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        sources_articles,
        names="sentiment_label_by_description",
        title="Sentiment Labels For Descriptions",
    )
    st.plotly_chart(fig2, use_container_width=True)


# Sentiment Over Time (Line Charts)
st.subheader("Sentiment Over Time")

sources_articles["date"] = sources_articles["published_at"].dt.date

daily_sentiment = (
    sources_articles.groupby("date")["overall_sentiment_by_title"]
    .mean()
    .reset_index()
)

daily_sentiment["date"] = pd.to_datetime(daily_sentiment["date"])

daily_count = (
    sources_articles.groupby("date")["id"]
    .count()
    .reset_index()
    .rename(columns={"id": "article_count"})
)

daily_count["date"] = pd.to_datetime(daily_count["date"])
max_days = (daily_sentiment["date"].max() - daily_sentiment["date"].min()).days
days_back = st.slider(
    "Days Back", min_value=2, max_value=max_days, value=max_days
)
threshold = daily_sentiment["date"].max() - pd.Timedelta(days=days_back)

filtered_sentiment = daily_sentiment[daily_sentiment["date"] >= threshold]
filtered_count = daily_count[daily_count["date"] >= threshold]

fig_sent = px.line(
    filtered_sentiment,
    x="date",
    y="overall_sentiment_by_title",
    title="Average Sentiment Over Time For Titles",
)
st.plotly_chart(fig_sent, use_container_width=True)

fig_count = px.line(
    filtered_count,
    x="date",
    y="article_count",
    title="Number of Articles Per Day",
)
st.plotly_chart(fig_count, use_container_width=True)

# Sentiment By Category (Bar Charts)
st.subheader("Average Sentiment by Category")

category_sentiment = (
    sources_articles.groupby("category")[
        ["overall_sentiment_by_title", "overall_sentiment_by_description"]
    ]
    .mean()
    .reset_index()
)

fig_cat = px.bar(
    category_sentiment,
    x="category",
    y=["overall_sentiment_by_title", "overall_sentiment_by_description"],
    title="Average Sentiment by Category",
    barmode="group",
    labels={
        "value": "Average Sentiment",
        "category": "Category",
        "variable": "Sentiment Type",
    },
)
st.plotly_chart(fig_cat, use_container_width=True)

# Sentiment by Source (Bar Charts With Filtering)
st.subheader("Sentiment by Source")

source_sentiment = (
    sources_articles.groupby("source_name")["overall_sentiment_by_title"]
    .mean()
    .reset_index()
    .rename(columns={"overall_sentiment_by_title": "avg_sentiment"})
)

option = st.radio(
    "View:", ("Top 10 Positive Sources", "Bottom 10 Negative Sources")
)

if option == "Top 10 Positive Sources":
    top_sources = source_sentiment.sort_values(
        by="avg_sentiment", ascending=False
    ).head(10)
else:
    top_sources = source_sentiment.sort_values(
        by="avg_sentiment", ascending=True
    ).head(10)

fig_sources = px.bar(
    top_sources,
    x="avg_sentiment",
    y="source_name",
    orientation="h",
    title=option,
    labels={"avg_sentiment": "Average Sentiment", "source_name": "Source"},
    text="avg_sentiment",
)
fig_sources.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_sources, use_container_width=True)
