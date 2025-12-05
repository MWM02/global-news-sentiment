# Global News Sentiment Analysis

A Python-based ETL project to extract, transform, and analyse global news articles to measure sentiment trends across sources, authors, and categories. The project includes a Streamlit dashboard for interactive exploration of the dataset.

---

## **Table of Contents**

- [Global News Sentiment Analysis](#global-news-sentiment-analysis)
  - [**Table of Contents**](#table-of-contents)
  - [**Goals**](#goals)
  - [**Choice of Data**](#choice-of-data)
  - [**Setup and Usage**](#setup-and-usage)
    - [**Requirements**](#requirements)
    - [**Installation**](#installation)
    - [**Environmental Setup**](#environmental-setup)
    - [**Running/Testing ETL**](#runningtesting-etl)
  - [**Challenges and Takeaways**](#challenges-and-takeaways)
  - [**Future Development**](#future-development)

---

## **Goals**

- Build a fully functional ETL pipeline that can cycle and collect data over time.
- Enrich the data with sentiment analysis on titles and descriptions of articles.
- Provide a visual, interactive dashboard for analysis using Streamlit.

---

## **Choice of Data**

The dataset is sourced from NewsAPI.org, which provides easy access with only an API key, up to 100 requests per day, and up to 100 results per request. Articles from the previous 30 days are available, with only a one-day delay.

The data comes from two main endpoints:

- **Sources** (`https://newsapi.org/docs/endpoints/sources`):  
  Columns: `id`, `name`, `description`, `url`, `category`, `language`, `country`

- **Articles** (`https://newsapi.org/docs/endpoints/everything`):  
  Columns: `author`, `title`, `description`, `url`, `urlToImage`, `publishedAt`, `content`, `source_id`, `source_name`

When running in a **test environment**, the ETL uses previously aggregated in `data/raw` data to avoid API calls. In **development mode**, the ETL fetches data from the API and saves/appends the collected data locally in `data/raw`.

---

## **Setup and Usage**

### **Requirements**

- Dependencies listed in `requirements.txt` or `pyproject.toml`

### **Installation**

```bash
# Clone the repository
git clone https://github.com/MWM02/global-news-sentiment.git
cd global-news-sentiment

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install project in editable mode
pip install -e .
```

### **Environmental Setup**

Create a development environment file `.env.dev`:

```env
NEWSAPI_KEY="YOUR_API_KEY"
NEWSAPI_REQUEST_LIMIT=90
NEWSAPI_REQUEST_INTERVAL_SECONDS=15
MAX_ARTICLE_AGE_DAYS=40
DAYS_BACK=2
CYCLE_NUMBER=2
CYCLE_INTERVAL_HOURS=24
```

Create a test environment file `.env.test`:

```env
MAX_ARTICLE_AGE_DAYS=40
CYCLE_NUMBER=1
```

### **Running/Testing ETL**

```bash
# To run in development mode
run_etl dev

# To run in test mode
run_etl test

# To run tests
run_tests unit # Current test options: unit
```

---

## **Challenges and Takeaways**

- **Data Quality:** The author column in articles was extremely inconsistent in format and quality making it difficult to clean effectively.
- **Sentiment Analysis Limitations:** NLTK Vader used for enriching data with sentiment scores could only analyse data in English.
- **Time Constraints:** The tight deadline made it harder to meet some of the user stories, like uploading to database, having unit tests for all ETL functions, and having doc strings in all large functions

---

## **Future Development**

- **Author Analysis:** Extend the dashboard to explore authors, including their average sentiment and potential collaboration networks.
- **Complete Testing:** Include different types of testing like end-to-end and integration tests.
- **Automated Deployment:** Set up a virtual machine with a cloud database and hosted dashboard for "live", continuously updated analysis.
