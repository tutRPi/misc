from dotenv import load_dotenv
load_dotenv()

import logging
from google.cloud import bigquery
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.db.session import SessionLocal

from app.services.bigquery_service import bq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")

        logger.info("Creating Bigquery Table")
        # create biquery table, if not exists
        schema = [
            bigquery.SchemaField("tpep_pickup_datetime", "DATETIME", mode="REQUIRED"),
            bigquery.SchemaField("tpep_dropoff_datetime", "DATETIME", mode="REQUIRED"),
            bigquery.SchemaField("passenger_count", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("trip_distance", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("best_route_distance", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("payment_type", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("tip_amount", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("total_amount", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("pickup_city", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("pickup_country", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("pickup_latitude", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("pickup_longitude", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("dropoff_latitude", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("dropoff_longitude", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("temperature_celsius", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("humidity", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("precip", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("weather_description", "STRING", mode="REQUIRED"),
        ]
        bq_table = bq.create_table(schema)

        logger.info("BigQuery Table created with table ID: {}".format(bq_table.full_table_id))

    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
