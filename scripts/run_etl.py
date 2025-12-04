import os
import sys
import time
from config.etl_config import load_etl_config
from config.api_config import load_api_config
from config.storage_config import load_storage_config
from config.types import ETLPipelineConfigs
from config.env_config import setup_env
from src.extract.extract import extract_data
from src.transform.transform import transform_data
from src.load.load import load_data
from src.analyse.analyse import launch_streamlit_app
from src.utils.logging_utils import setup_logger

logger = setup_logger("etl_pipeline", "etl_pipeline.log")


def run_etl_cycle(env: str, configs: ETLPipelineConfigs) -> None:
    logger.info(f"Starting ETL cycle for environment: {env}")

    try:
        logger.info("Running extraction phase")
        extracted_data = extract_data(env, configs)
        logger.info("Data extraction complete")

        logger.info("Running transformation phase")
        transformed_data = transform_data(
            extracted_data,
            max_article_age_days=configs["etl"]["max_article_age_days"],
        )
        logger.info("Data transformation complete")

        logger.info("Running load phase")
        load_data(transformed_data, configs["storage"])
        logger.info("Data load complete")

        logger.info("ETL pipeline completed successfully")

    except Exception as e:
        logger.error(f"ETL cycle failed in {env} environment: {e}")
        sys.exit(1)


def main() -> None:
    setup_env(sys.argv)
    env = os.getenv("ENV")

    if env is None:
        raise EnvironmentError("The ENV environment variable is not set!")

    configs = {
        "etl": load_etl_config(),
        "storage": load_storage_config(),
    }

    if env == "dev":
        configs["api"] = load_api_config()

    num_of_cycles = configs["etl"]["cycle_num"]
    cycle_interval_hours = configs["etl"]["cycle_interval_hours"]
    cycle_interval_seconds = cycle_interval_hours * 3600

    for cycle in range(1, num_of_cycles + 1):
        run_etl_cycle(env, configs)

        logger.info(
            f"ETL cycle {cycle}/{num_of_cycles} complete. "
            f"Waiting {cycle_interval_hours} hours until next cycle..."
        )

        if cycle < num_of_cycles:
            time.sleep(cycle_interval_seconds)

    logger.info("All ETL cycles completed.")

    logger.info("Starting analysis phase")
    launch_streamlit_app()
    logger.info("Launched Streamlit application")


if __name__ == "__main__":
    main()
