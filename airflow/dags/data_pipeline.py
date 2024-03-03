import datetime

import pendulum
from tasks import extract, load, transform

from airflow.decorators import dag


@dag(
    dag_id="data-pipeline",
    schedule_interval="@hourly",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def data_pipeline():
    # Crawl data
    raw_law_documents = extract()
    # Clean data
    cleaned_law_documents = transform(raw_law_documents)
    # store data
    load(cleaned_law_documents)


dag = data_pipeline()
