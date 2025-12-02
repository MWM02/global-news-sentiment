import requests
from typing import Dict, Any


class ApiError(Exception):
    """Base exception for API errors."""

    pass


class RateLimitedError(ApiError):
    """Raised when the API returns a rate-limited response."""

    pass


class InvalidApiKeyError(ApiError):
    """Raised when API key is invalid, missing, or disabled."""

    pass


class ParameterError(ApiError):
    """Raised when request parameters are invalid or missing."""

    pass


ERROR_CODE_MAPPING = {
    "rateLimited": RateLimitedError,
    "apiKeyDisabled": InvalidApiKeyError,
    "apiKeyInvalid": InvalidApiKeyError,
    "apiKeyMissing": InvalidApiKeyError,
    "apiKeyExhausted": InvalidApiKeyError,
    "parameterInvalid": ParameterError,
    "parametersMissing": ParameterError,
    "sourcesTooMany": ParameterError,
    "sourceDoesNotExist": ParameterError,
}


def handle_api_response(response: requests.Response) -> Dict[str, Any]:
    try:
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ApiError(f"HTTP request failed: {e}")
    except ValueError:
        raise ApiError("Response contains invalid JSON.")

    if data.get("status") != "ok":
        code = data.get("code", "unexpectedError")
        message = data.get("message", "Unknown API error")
        exception_class = ERROR_CODE_MAPPING.get(code, ApiError)
        raise exception_class(message)

    return data
