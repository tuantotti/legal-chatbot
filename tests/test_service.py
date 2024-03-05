from utils.logger import Logger
from rest_api.services.service import save_law
import json
from rest_api.services.db import MongoClientClass
import asyncio
import pytest
from rest_api.schemas.item import LawItem

logger = Logger.get_logger()

class TestService:
    @pytest.mark.asyncio
    async def test_bulk_insert_law_json(self):
        with open("crawler/output/law_document.json") as file:
            laws = json.load(file)
            
        ids = await save_law(laws=laws, collection_name="law-collection-test")
        logger.info(ids.inserted_ids)
        
    @pytest.mark.asyncio
    async def test_bulk_insert_law_item(self):
        laws = [LawItem(
                0,
                "news_code",
                [],
                "content",
            ), LawItem(
                1,
                "news_code",
                [],
                "content",
            )]
        logger.info(type(laws[0]))
        ids = await save_law(laws=laws, collection_name="law-collection-test")
        logger.info(ids.inserted_ids)
        
        
