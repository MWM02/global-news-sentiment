import pytest
import pandas as pd
from unittest.mock import MagicMock
from config.api_config import ApiConfig
from src.utils.date_utils import get_article_date_str
from src.extract.extract_articles import (
    extract_articles,
    extract_articles_for_source_execution,
    TYPE,
    EXPECTED_IMPORT_RATE,
)


@pytest.fixture
def api_config() -> ApiConfig:
    return ApiConfig(
        api_key="test-key",
        language="en",
        sort_by="popularity",
        request_limit=99,
        interval_seconds=30,
        days_before=2,
        base_url="https://newsapi.org/v2",
        sources_endpoint="/top-headlines/sources",
        articles_endpoint="/everything",
    )


@pytest.fixture
def mock_log_extract_success(mocker):
    return mocker.patch("src.extract.extract_articles.log_extract_success")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.extract.extract_articles.logger")


@pytest.fixture
def mock_sources_df():
    return pd.DataFrame(
        [
            {
                "id": "abc-news",
                "name": "ABC News",
                "description": "Some description",
                "url": "https://abcnews.go.com",
                "category": "general",
                "language": "en",
                "country": "us",
            }
        ]
    )


@pytest.fixture
def successful_response_with_results():
    return {
        "status": "ok",
        "totalResults": 2,
        "articles": [
            {
                "source": {"id": "abc-news", "name": "ABC News"},
                "author": "test_user",
                "title": "Test title 1",
                "description": "Test description 1",
                "url": "https://test1.com",
                "urlToImage": "https://test_image.com",
                "publishedAt": "2025-12-01T20:07:40Z",
                "content": "..........",
            },
            {
                "source": {"id": "abc-news", "name": "ABC News"},
                "author": "test_user",
                "title": "Test title 2",
                "description": "Test description 2",
                "url": "https://test2.com",
                "urlToImage": "https://test_image.com",
                "publishedAt": "2025-12-01T20:06:10Z",
                "content": "..........",
            },
        ],
    }


def test_log_extract_articles_success(
    mocker, mock_log_extract_success, mock_logger, mock_sources_df, api_config
):
    mock_execution_time = 0.5
    mock_df = pd.DataFrame(
        [
            {
                "source": {"id": "fortune", "name": "Fortune"},
                "author": "test_user",
                "title": "Test title",
                "description": "Test description 1",
                "url": "https://test.com",
                "urlToImage": "https://test_image.com",
                "publishedAt": "2025-12-01T20:07:40Z",
                "content": "..........",
            },
            {
                "source": {
                    "id": "the-times-of-india",
                    "name": "The Times of India",
                },
                "author": "test_user",
                "title": "Test title",
                "description": "Test description 2",
                "url": "https://test.com",
                "urlToImage": "https://test_image.com",
                "publishedAt": "2025-12-01T20:06:10Z",
                "content": "..........",
            },
        ],
    )
    mocker.patch(
        "src.extract.extract_articles.extract_articles_for_source_execution",
        return_value=mock_df,
    )
    mock_start_time = 10
    mock_end_time = 10.5
    mocker.patch(
        "src.extract.extract_articles.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time],
    )
    mocker.patch("src.extract.extract_articles.time.sleep")

    df = extract_articles(mock_sources_df, api_config)

    mock_log_extract_success.assert_called_once_with(
        mock_logger,
        TYPE,
        df.shape,
        mock_execution_time,
        expected_rate=EXPECTED_IMPORT_RATE,
    )


def test_extract_articles_empty_sources_logs_warning(mock_logger, api_config):
    empty_df = pd.DataFrame()

    result = extract_articles(empty_df, api_config)

    assert result.empty
    mock_logger.warning.assert_called_once_with(
        "No sources provided. Returning empty articles DataFrame."
    )


@pytest.mark.parametrize(
    "num_sources, request_limit, expected_calls",
    [
        (1, 2, 1),
        (3, 2, 2),
        (5, 3, 3),
        (4, 10, 4),
    ],
)
def test_extract_articles_with_different_request_limits(
    mocker,
    api_config,
    mock_logger,
    mock_log_extract_success,
    num_sources,
    request_limit,
    expected_calls,
):
    mock_sources_df = pd.DataFrame(
        [
            {"id": f"source_{i}", "name": f"Source {i}"}
            for i in range(num_sources)
        ]
    )
    mock_articles_df = pd.DataFrame({"articles": ["x", "y"]})
    api_config["request_limit"] = request_limit
    mock_articles_for_source_execution = mocker.patch(
        "src.extract.extract_articles.extract_articles_for_source_execution",
        return_value=mock_articles_df,
    )
    mock_sleep = mocker.patch("src.extract.extract_articles.time.sleep")

    extract_articles(mock_sources_df, api_config)

    assert mock_articles_for_source_execution.call_count == expected_calls
    assert mock_sleep.call_count == expected_calls - 1


def test_extract_articles_logs_no_articles_for_source(
    mocker, mock_logger, mock_sources_df, api_config
):
    mock_empty_df = pd.DataFrame()
    mocker.patch(
        "src.extract.extract_articles.extract_articles_for_source_execution",
        return_value=mock_empty_df,
    )

    extract_articles(mock_sources_df, api_config)

    mock_logger.info.assert_any_call(
        "No articles returned for source abc-news"
    )


def test_extract_articles_handles_exception(
    mocker, mock_logger, mock_log_extract_success, api_config, mock_sources_df
):
    mocker.patch(
        "src.extract.extract_articles.extract_articles_for_source_execution",
        side_effect=Exception("API failure"),
    )

    df = extract_articles(mock_sources_df, api_config)

    assert df.empty
    mock_logger.error.assert_called_once_with(
        "Failed to fetch articles for source abc-news: API failure"
    )
    mock_log_extract_success.assert_not_called()


def test_extract_articles_for_source_execute_returns_df_for_valid_response(
    mocker, api_config, successful_response_with_results
):
    mock_response = MagicMock()
    mocker.patch(
        "src.extract.extract_articles.requests.get", return_value=mock_response
    )
    mocker.patch(
        "src.extract.extract_articles.handle_api_response",
        return_value=successful_response_with_results,
    )

    df = extract_articles_for_source_execution(
        api_config, "test-source", "2025-12-02"
    )

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert list(df.columns) == [
        "author",
        "title",
        "description",
        "url",
        "urlToImage",
        "publishedAt",
        "content",
        "source_id",
        "source_name",
    ]


def test_extract_articles_for_source_execute_returns_empty_df_when_no_articles(
    mocker, api_config
):
    mock_response = MagicMock()
    mocker.patch(
        "src.extract.extract_articles.requests.get", return_value=mock_response
    )
    mocker.patch(
        "src.extract.extract_articles.handle_api_response",
        return_value={"articles": []},
    )

    df = extract_articles_for_source_execution(
        api_config, "test-source", "2025-12-02"
    )

    assert df.empty


def test_extract_articles_for_source_execution_requests_with_correct_args(
    mocker, mock_sources_df, api_config, successful_response_with_results
):
    mock_source_id = mock_sources_df["id"].astype(str)
    date_str = get_article_date_str(api_config)
    expected_url = f"{api_config['base_url']}{api_config['articles_endpoint']}"
    expected_params = {
        "apiKey": api_config["api_key"],
        "language": api_config["language"],
        "sortBy": api_config["sort_by"],
        "from": date_str,
        "to": date_str,
        "sources": mock_source_id,
    }
    mock_response = MagicMock()
    mock_get = mocker.patch(
        "src.extract.extract_sources.requests.get",
        return_value=mock_response,
    )
    mock_handle_api_response = mocker.patch(
        "src.extract.extract_articles.handle_api_response",
        return_value=successful_response_with_results,
    )
    extract_articles_for_source_execution(api_config, mock_source_id, date_str)

    mock_get.assert_called_once_with(
        expected_url,
        params=expected_params,
        timeout=10,
    )
    mock_handle_api_response.assert_called_once_with(mock_response)
