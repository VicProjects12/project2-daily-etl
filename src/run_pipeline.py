
import datetime
import logging
import pathlib

from src.extract import extract
from src.transform import transform
from src.load import load


def configure_logging():
    # Create the logs folder if it does not exist
    pathlib.Path("logs").mkdir(parents=True, exist_ok=True)

    # Configure logging to write to both the terminal and a file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log", encoding="utf-8"),
            logging.StreamHandler()
        ],
    )


def run_pipeline():
    logger = logging.getLogger(__name__)

    # Use today's date for the raw filename
    day = datetime.date.today().isoformat()

    logger.info("========== PIPELINE STARTED ==========")

    try:
        # Step 1: Extract
        logger.info("Starting extraction...")
        extract(day)
        logger.info("Extraction completed.")

        # Step 2: Transform and validate
        logger.info("Starting transformation and validation...")
        transform(day)
        logger.info("Transformation and validation completed.")

        # Step 3: Load
        logger.info("Starting database loading...")
        load()
        logger.info("Database loading completed.")

        logger.info("========== PIPELINE COMPLETED SUCCESSFULLY ==========")

    except Exception:
        logger.exception("PIPELINE FAILED")
        raise


if __name__ == "__main__":
    configure_logging()
    run_pipeline()
