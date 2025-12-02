import pytest
import pandas as pd
from unittest.mock import MagicMock
from config.api_config import ApiConfig
from src.extract.extract_sources import (
    extract_sources,
    extract_sources_execution,
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
    return mocker.patch("src.extract.extract_sources.log_extract_success")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.extract.extract_sources.logger")


@pytest.fixture
def successful_response_with_results():
    """Mocked API response containing two sources."""
    return {
        "status": "ok",
        "sources": [
            {
                "id": "abc-news",
                "name": "ABC News",
                "description": "Some description",
                "url": "https://abcnews.go.com",
                "category": "general",
                "language": "en",
                "country": "us",
            },
            {
                "id": "bbc-news",
                "name": "BBC News",
                "description": "Another description",
                "url": "https://bbc.co.uk/news",
                "category": "general",
                "language": "en",
                "country": "gb",
            },
        ],
    }


def test_log_extract_sources_success(
    mocker, mock_log_extract_success, mock_logger
):
    mock_execution_time = 0.5
    mock_df = pd.DataFrame(
        [
            {
                "id": "abc-news",
                "name": "ABC News",
                "description": "Some description",
                "url": "https://abcnews.go.com",
                "category": "general",
                "language": "en",
                "country": "us",
            },
            {
                "id": "bbc-news",
                "name": "BBC News",
                "description": "Another description",
                "url": "https://bbc.co.uk/news",
                "category": "general",
                "language": "en",
                "country": "gb",
            },
        ]
    )
    mocker.patch(
        "src.extract.extract_sources.extract_sources_execution",
        return_value=mock_df,
    )
    mock_start_time = 10
    mock_end_time = 10.5
    mocker.patch(
        "src.extract.extract_sources.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time],
    )

    df = extract_sources(api_config)

    mock_log_extract_success.assert_called_once_with(
        mock_logger, TYPE, df.shape, mock_execution_time, EXPECTED_IMPORT_RATE
    )


def test_extract_sources_returns_empty_df_if_no_results(
    mocker, mock_logger, api_config
):
    mock_df = pd.DataFrame()
    mocker.patch(
        "src.extract.extract_sources.extract_sources_execution",
        return_value=mock_df,
    )
    mock_warn = mocker.patch("src.extract.extract_sources.logger.warning")

    result = extract_sources(api_config)

    assert result.empty
    mock_warn.assert_called_once_with("No sources returned from API.")


def test_extract_sources_error(mocker, mock_logger, api_config):
    mocker.patch(
        "src.extract.extract_sources.extract_sources_execution",
        side_effect=Exception("Exception message"),
    )

    with pytest.raises(Exception, match="Exception message"):
        extract_sources(api_config)

    mock_logger.error.assert_called_once_with(
        "Failed to extract sources: Exception message"
    )


def test_extract_sources_execution_returns_df_for_valid_response(
    mocker, api_config, successful_response_with_results
):
    mock_response = MagicMock()
    mocker.patch(
        "src.extract.extract_sources.requests.get", return_value=mock_response
    )
    mocker.patch(
        "src.extract.extract_sources.handle_api_response",
        return_value=successful_response_with_results,
    )

    df = extract_sources_execution(api_config)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert list(df.columns) == [
        "id",
        "name",
        "description",
        "url",
        "category",
        "language",
        "country",
    ]


def test_extract_sources_execution_calls_requests_with_correct_args(
    mocker, api_config, successful_response_with_results
):
    expected_url = f"{api_config['base_url']}{api_config['sources_endpoint']}"
    expected_params = {
        "apiKey": api_config["api_key"],
        "language": api_config["language"],
    }
    mock_response = MagicMock()
    mock_get = mocker.patch(
        "src.extract.extract_sources.requests.get",
        return_value=mock_response,
    )
    mock_handle_api_response = mocker.patch(
        "src.extract.extract_sources.handle_api_response",
        return_value=successful_response_with_results,
    )

    extract_sources_execution(api_config)

    mock_get.assert_called_once_with(
        expected_url,
        params=expected_params,
        timeout=10,
    )
    mock_handle_api_response.assert_called_once_with(mock_response)
