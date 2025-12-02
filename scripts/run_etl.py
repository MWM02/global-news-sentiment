import os
import sys
import time
from logging import Logger
from config.env_config import setup_env
from src.extract.extract import extract_data
from src.utils.logging_utils import setup_logger


def run_daily_cycle(env: str, logger: Logger) -> None:
    logger.info(f"Starting ETL cycle for environment: {env}")

    try:
        # Extract phase
        logger.info("Running extraction phase")
        extracted_data = extract_data()
        sources, articles = extracted_data
        logger.info("Data extraction complete")

        # Transform phase
        # Load phase

        logger.info("ETL pipeline completed successfully")

    except Exception as e:
        logger.error(f"ETL cycle failed in {env} environment: {e}")
        sys.exit(1)


def main() -> None:
    setup_env(sys.argv)
    env = os.getenv("ENV", "unknown")
    logger = setup_logger("etl_pipeline", "etl_pipeline.log")

    while True:
        run_daily_cycle(env, logger)
        logger.info("ETL cycle complete. Waiting 24 hours until next cycle...")
        time.sleep(24 * 60 * 60)


if __name__ == "__main__":
    main()
