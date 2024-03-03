from pymongo import errors
from pymongo.mongo_client import MongoClient

from configs.config import settings
from utils.logger import Logger

logger = Logger.get_logger()


class MongoClientClass:
    def __init__(self) -> None:
        self.mongo_uri = settings.MONGO_URI
        self.mongo_database = settings.MONGO_DATABASE
        self.client = self.get_client()

    def get_client(self) -> MongoClient:
        client = None
        try:
            if self.mongo_uri:
                client = MongoClient(self.mongo_uri)
        except errors.ConnectionFailure as e:
            logger.error(f"Connection failure: {e}")
        except Exception as e:
            logger.error(f"{e}")

        return client


class MilvusClientClass:
    def __init__(self) -> None:
        pass
