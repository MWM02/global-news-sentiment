# USER REQUIREMENTS

## Project Requirements

A user requires a robust ETL pipeline and analysis dashboard to track and explore sentiment trends across global news sources. The system should extract articles and sources from NewsAPI endpoints, transform the data by cleaning, normalising, and enriching it (with sentiment analysis), and load the processed data locally and into a database. The system should also support multiple ETL cycles according to user-defined intervals. Finally, an interactive dashboard should provide sentiment insights, comparisons across sources and categories, and allow exploration of top and bottom performing sources.

---

## EPIC 1: Data Extraction & Transformation

**As a user**,  
I want to extract news sources and articles from NewsAPI and transform the data by cleaning, normalising, and enriching it,  
So that I can analyse high-quality, consistent data.

### Epic 1 Breakdown

#### User Story 1

**As a user**,  
I want to extract sources and articles from NewsAPI,  
So that raw data is available for processing and analysis.

**Acceptance Criteria:**

- Sources and articles are retrieved from the NewsAPI endpoints.
- API key is loaded securely from environment/config file.
- Extraction handles errors and rate limits gracefully.
- Extracted data is stored in a Pandas DataFrame.
- Local test mode skips API calls and uses saved CSVs.

#### User Story 2

**As a user**,  
I want to clean, normalise, and enrich the extracted data (including sentiment analysis),  
So that I can analyse consistent, high-quality data.

**Acceptance Criteria:**

- Duplicate articles and sources are removed.
- Missing or invalid data (titles, descriptions, published dates) are handled.
- Dates are normalised to datetime objects.
- Columns are renamed consistently.
- Sentiment scores and labels are calculated for titles and descriptions.

---

## EPIC 2: Data Load & ETL Cycles

**As a user**,  
I want to save the processed data locally and in a database, and run multiple ETL cycles,  
So that the dataset stays up-to-date and is readily accessible for analysis.

### Epic 2 Breakdown

#### User Story 3

**As a user**,  
I want to save transformed and enriched data to CSV files and a database,  
So that it can be reused or queried efficiently.

**Acceptance Criteria:**

- Data is saved to `data/processed/` and loaded into the database.
- Save operations handle errors gracefully and are logged.

#### User Story 4

**As a user**,  
I want the ETL pipeline to run multiple cycles with configurable intervals,  
So that the dataset remains up-to-date automatically.

**Acceptance Criteria:**

- ETL cycles can be configured via `etl_config`.
- Interval between cycles is respected.
- Logs capture each cycle’s success or failure.

---

## EPIC 3: Analysis & Visualisation

**As a user**,  
I want an interactive dashboard that displays sentiment trends, comparisons across sources and categories,  
So that I can explore insights about global news coverage.

### Epic 3 Breakdown

#### User Story 5

**As a user**,  
I want to see overall sentiment metrics and distributions,  
So that I can get a quick understanding of news sentiment.

**Acceptance Criteria:**

- Dashboard shows number of sources, number of articles, and average sentiment by title and description.
- Pie charts display sentiment label distributions for titles and descriptions.

#### User Story 6

**As a user**,  
I want to explore sentiment over time and by category,  
So that I can detect trends and compare topics.

**Acceptance Criteria:**

- Line chart displays average sentiment per day for titles and descriptions.
- Bar chart displays average sentiment per category.
- Slider allows the user to select the number of days to visualise.

#### User Story 7

**As a user**,  
I want to see top and bottom sources by average sentiment,  
So that I can identify the most positive or negative news outlets.

**Acceptance Criteria:**

- Bar chart shows top 10 and bottom 10 sources by average sentiment.
- Data updates dynamically if filters are applied.
