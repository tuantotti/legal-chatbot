from typing import List

from rest_api.schemas.item import LawItem
from rest_api.services.db import MongoClientClass

mongo_client = MongoClientClass().client


async def save_law_item(law_item: List[LawItem]):
    pass
