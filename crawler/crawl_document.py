import datetime
import multiprocessing
import re
import time
from typing import Any, Dict, List, Union

import click
import requests
import yaml
from tqdm import tqdm

from rest_api.schemas.item import (LawItem, LawOrganizationItem,
                                   LawQuestionAnswerPairItem, LawStatusItem)
from utils.logger import Logger
from utils.save_file import save_file

logger = Logger.get_logger()


class CrawlData:
    """
    Crawl legal documents from lawnet.vn
    """

    def __init__(
        self,
        num_workers: int,
        output_dir: str,
        start_date: Union[datetime.datetime, str],
        end_date: Union[datetime.datetime, str],
    ) -> None:
        """Initial objects

        Args:
            num_workers (int): number of workers
            output_dir (str): output dir to save file
        """
        self.num_workers = num_workers
        self.output_dir = output_dir
        self.start_date = start_date
        self.end_date = end_date
        logger.info(f"start_date: {start_date}, end_date: {end_date}")
        with open("configs/lawnet_api.yaml", "r") as file:
            law_config = yaml.safe_load(file)

        self.search_law_params = law_config["law-search"]
        self.law_status_params = law_config["law-status"]
        self.law_organization_params = law_config["law-organization"]
        self.law_detail_params = law_config["law-detail"]
        self.list_question_by_lawid_params = law_config["list-question-by-lawid"]
        self.suggest_by_law_params = law_config["suggest-by-law"]

    def get_law_documents(self) -> List[LawItem]:
        """Crawl legal documents from lawnet

        Some errors:
        + HTTPSConnectionPool: some laws does not have questions --> call api --> error (take time because of retrying call)
        + Api return law with id = 0 with all required fields is None --> error when call convert_raw_to_item

        Returns:
            List[LawItem]: list of converted documents
        """
        record_list = []
        law_detail_list = []

        self.search_law_params["body"]["bday"] = str(self.start_date)
        self.search_law_params["body"]["eday"] = str(self.end_date)
        raw_documents = self.process_request(self.search_law_params)
        if raw_documents:
            total_items = raw_documents["Data"]["TotalItems"]
            num_pages = (
                int(total_items / 20)
                if total_items % 20 == 0
                else int(total_items / 20) + 1
            )

            with multiprocessing.get_context("fork").Pool(
                processes=self.num_workers
            ) as pool:
                for page in tqdm(range(1, num_pages + 1, 1)):
                    law_detail_result = pool.apply_async(
                        self.get_law_document_by_page, args=(page,)
                    )

                    law_detail_list.append(law_detail_result)

                [
                    record_list.extend(law_detail.get())
                    for law_detail in tqdm(
                        law_detail_list, total=len(law_detail_list), position=0
                    )
                ]

            logger.info(f"Crawl {len(record_list)} / {total_items} law documents")

        return record_list

    def get_law_document_by_page(self, page: int) -> List[LawItem]:
        """Get legal documents with specific page

        Args:
            page (int): page number

        Returns:
            List[LawItem]: list of converted documents
        """
        self.search_law_params["body"]["page"] = page
        raw_documents = self.process_request(self.search_law_params)
        new_page_law_list = []
        if raw_documents:
            law_id_list = [law["LawID"] for law in raw_documents["Data"]["Documents"]]
            new_page_law_list = [
                law_detail
                for id in law_id_list
                if (law_detail := self.get_law_detail(id))
            ]

        return new_page_law_list

    def get_law_status(self) -> List[LawStatusItem]:
        """Get all law status

        Returns:
            List[LawStatusItem]: list of law status
        """
        raw_status_list = self.process_request(self.law_status_params)
        if raw_status_list:
            raw_status_list = [
                LawStatusItem(
                    law_status["Status_ID"],
                    law_status["Status_Name"],
                    law_status["EntityState"],
                )
                for law_status in raw_status_list
            ]
        else:
            raw_status_list = []

        return raw_status_list

    def get_law_organization(self) -> List[LawOrganizationItem]:
        """Get list of organizations that create legal documents

        Returns:
            List[LawOrganizationItem]: list of organizations
        """
        raw_organization_list = self.process_request(self.law_organization_params)
        if raw_organization_list:
            raw_organization_list = [
                LawOrganizationItem(
                    law_organization["OrgID"],
                    law_organization["OrgName"],
                    law_organization["UuTien"],
                    law_organization["EntityState"],
                )
                for law_organization in raw_organization_list
            ]
        else:
            raw_organization_list = []

        return raw_organization_list

    def get_law_detail(self, law_id: int) -> LawItem:
        """Get the detail of legal documents

        Args:
            law_id (int): id of law

        Returns:
            LawItem: a legal document
        """
        law_detail_item = None
        law_detail_params = self.law_detail_params
        law_detail_params["params"]["LawID"] = law_id

        # call api
        law_detail = self.process_request(law_detail_params)

        if law_detail:
            law_detail_item = self.convert_raw_to_item(law_detail)

        return law_detail_item

    def get_question_by_law_id(self, law_id: int) -> List[LawQuestionAnswerPairItem]:
        """Get question corresponding to law id

        Args:
            law_id (int): law id

        Returns:
            List: list of question corresponding to law
        """
        question_answer_pair_list = []
        question_answer_pair_item_list = []
        list_question_by_lawid_params = self.list_question_by_lawid_params
        list_question_by_lawid_params["params"]["lawId"] = law_id

        # Some laws does not have question -> Connection Error
        list_question_by_lawid_params["params"]["type"] = 1
        question_answer_pair_type_1_list = self.process_request(
            list_question_by_lawid_params
        )

        # Some laws does not have question -> Connection Error
        list_question_by_lawid_params["params"]["type"] = 2
        question_answer_pair_type_2_list = self.process_request(
            list_question_by_lawid_params
        )

        if question_answer_pair_type_1_list:
            for question_answer_pair_type_1 in question_answer_pair_type_1_list:
                question_answer_pair_list.extend(
                    [
                        question_answer
                        for question_answer in question_answer_pair_type_1[
                            "listBaiViet"
                        ]
                    ]
                )

        if question_answer_pair_type_2_list:
            for question_answer_pair_type_2 in question_answer_pair_type_2_list:
                question_answer_pair_list.extend(
                    [
                        question_answer
                        for question_answer in question_answer_pair_type_2[
                            "listBaiViet"
                        ]
                    ]
                )
        if question_answer_pair_list:
            question_answer_pair_item_list = [
                LawQuestionAnswerPairItem(
                    law_id, bai_viet["Title"], "", bai_viet["Url"]
                )
                for bai_viet in question_answer_pair_list
            ]

        return question_answer_pair_item_list

    def suggest_law_by_id(self, law_id: int) -> List:
        """Get suggested laws by law id

        Args:
            law_id (int): law id

        Returns:
            List: list of suggested laws
        """
        suggest_by_law_params = self.suggest_by_law_params
        suggest_by_law_params["params"]["LawID"] = law_id
        # call api from lawnet
        result = self.process_request(suggest_by_law_params)

        return result

    def convert_raw_to_item(self, law: Dict) -> LawItem:
        try:
            # logger.info(question_answer_pair)
            # logger.info(law)
            law_id = law["Document"]["LawID"]
            news_code = law["Document"]["News_Code"]
            content = law.get("ContentVN", "")

            law_item = LawItem(
                law_id,
                news_code,
                [],
                content,
            )
        except Exception as e:
            logger.error(f"{e} with law id {law_id}")
            law_item = None

        return law_item

    def convert_str_to_date(self, date_str: str) -> datetime:
        date_result = None
        timestamp = re.search(r"[0-9]+", date_str)

        if timestamp:
            timestamp = int(timestamp.group(0)) / 1000  # convert to second
            date_result = datetime.fromtimestamp(timestamp)

        return date_result

    def convert_str_to_list(self, str: str):
        list_result = []
        list_match = re.search(r"[0-9]+", str)

        if list_match:
            list_result = [int(match) for match in list_match.groups()]

        return list_result

    def process_request(self, api_config: Dict) -> Any:
        """process the request from specific config

        Args:
            api_config (Dict): config of incoming request

        Returns:
            Any: response of request
        """
        result = None
        url = api_config["url"]
        method = api_config["method"]
        params = api_config.get("params", {})
        headers = api_config.get("headers", {})
        body = api_config.get("body", {})

        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method == "POST":
                response = requests.post(url, params=params, headers=headers, json=body)

            if response.status_code == 200:
                result = response.json()
            else:
                response.raise_for_status()
        except Exception as e:
            logger.error(f"{e}")

        return result

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        start_time = time.time()
        # crawl law documents
        law_documents = self.get_law_documents()
        end_time = time.time()
        logger.info(f"Crawled documents take: {end_time - start_time}")
        law_documents = [law.convert_to_json() for law in law_documents]
        save_file(law_documents, f"{self.output_dir}")


@click.command()
@click.option("--num_workers", "-np", default=8, help="Number of workers")
@click.option(
    "--output_dir",
    "-od",
    default="crawler/output/law_detail_documents.json",
    help="File to save output of crawled file",
)
@click.option(
    "--start_date",
    "-sd",
    default=str(datetime.date(1944, 1, 1)),
    help="Start date to crawl",
)
@click.option(
    "--end_date",
    "-ed",
    default=str(datetime.date.today()),
    help="File to save output of crawled file",
)
def run_crawl(
    num_workers: int = None,
    output_dir: str = None,
    start_date: Union[datetime.datetime, str] = str(datetime.date(1944, 1, 1)),
    end_date: Union[datetime.datetime, str] = str(datetime.date.today()),
) -> None:
    crawl_data = CrawlData(
        num_workers=num_workers,
        output_dir=output_dir,
        start_date=start_date,
        end_date=end_date,
    )
    crawl_data()


if __name__ == "__main__":
    run_crawl()
