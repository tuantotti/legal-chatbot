from typing import Dict, List, Union

from rest_api.schemas.item import LawItem
from rest_api.services.db import MongoClientClass

mongo_client = MongoClientClass().client


async def save_law(
    laws: Union[List[LawItem] | List[Dict]],
    database_name: str = "legal-chatbot",
    collection_name: str = "law-collection",
):
    if getattr(laws[0], "model_dump", None):
        laws = [law.model_dump() for law in laws]

    legal_chatbot_database = mongo_client[database_name]
    law_collection = legal_chatbot_database[collection_name]
    result = law_collection.insert_many(laws)
    return result
