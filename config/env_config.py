import os
from typing import List
from dotenv import load_dotenv

ENVS = ["test", "dev"]


def setup_env(argv: List[str]) -> None:
    if len(argv) != 2 or argv[1] not in ENVS:
        raise ValueError(
            "Please provide an environment: " f"{ENVS}. E.g. run_etl dev"
        )

    env = argv[1]

    cleanup_previous_env()
    os.environ["ENV"] = env

    env_file = f".env.{env}"

    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Environment file '{env_file}' not found")

    print(f"Loading environment variables from: {env_file}")
    load_dotenv(env_file, override=True)


def cleanup_previous_env() -> None:
    keys_to_clear = [
        "NEWSAPI_KEY",
        "NEWSAPI_REQUEST_LIMIT",
        "NEWSAPI_REQUEST_INTERVAL_SECONDS",
        "MAX_ARTICLE_AGE_DAYS",
        "DAYS_BACK",
        "CYCLE_NUMBER",
        "CYCLE_INTERVAL_HOURS",
    ]

    for key in keys_to_clear:
        if key in os.environ:
            del os.environ[key]
