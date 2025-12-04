import subprocess
from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__, "streamlit.log")


def launch_streamlit_app():
    try:
        logger.info("Launching Streamlit app...")
        subprocess.run(
            ["streamlit", "run", "src/analyse/streamlit_app.py"], check=True
        )
    except Exception as e:
        logger.error(f"Failed to launch Streamlit: {e}")
