from datetime import date, timedelta
from typing import List

from airflow.decorators import task
from crawler.crawl_document import CrawlData
from crawler.preprocessing import PreProcessing
from rest_api.schemas.item import LawItem


@task
def extract() -> List[LawItem]:
    # crawl data from lawnet from yesterday to today
    today = date.today()
    yesterday = today - timedelta(days=1)
    crawl_data = CrawlData(
        num_workers=8, start_date=str(yesterday), end_date=str(today)
    )

    return crawl_data.get_law_documents()


@task
def transform(law_list: List[LawItem]) -> List[LawItem]:
    # preprocessing and cleaning
    pass


@task
def load():
    # save to mongo database
    # encode and save to milvus database
    pass
