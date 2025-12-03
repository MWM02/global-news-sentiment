import os
import sys
import time
from config.etl_config import load_etl_config
from config.env_config import setup_env
from src.extract.extract import extract_data
from src.transform.transform import transform_data
from src.load.load import load_data
from src.utils.logging_utils import setup_logger

logger = setup_logger("etl_pipeline", "etl_pipeline.log")


def run_etl_cycle(env: str) -> None:
    logger.info(f"Starting ETL cycle for environment: {env}")

    try:
        logger.info("Running extraction phase")
        extracted_data = extract_data(env)
        logger.info("Data extraction complete")

        logger.info("Running transformation phase")
        transformed_data = transform_data(extracted_data)
        logger.info("Data transformation complete")

        logger.info("Running load phase")
        load_data(transformed_data)
        logger.info("Data load complete")

        logger.info("ETL pipeline completed successfully")

    except Exception as e:
        logger.error(f"ETL cycle failed in {env} environment: {e}")
        sys.exit(1)


def main() -> None:
    setup_env(sys.argv)
    etl_config = load_etl_config()
    env = os.getenv("ENV")

    num_of_cycles = etl_config["cycle_num"]
    cycle_interval_hours = etl_config["cycle_interval_hours"]
    cycle_interval_seconds = cycle_interval_hours * 60 * 60

    if env is None:
        raise EnvironmentError("The ENV environment variable is not set!")

    for cycle in range(1, num_of_cycles + 1):
        run_etl_cycle(env)

        logger.info(
            f"ETL cycle {cycle}/{num_of_cycles} complete. "
            f"Waiting {cycle_interval_hours} hours until next cycle..."
        )

        if cycle < num_of_cycles:
            time.sleep(cycle_interval_seconds)

    logger.info("All ETL cycles completed.")


if __name__ == "__main__":
    main()
