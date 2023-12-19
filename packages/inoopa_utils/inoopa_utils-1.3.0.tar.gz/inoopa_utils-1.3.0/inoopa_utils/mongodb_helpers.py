import os
from custom_types.companies import Company
from pymongo import MongoClient
from inoopa_logging import create_logger

class DbManager:
    """
    This class is used to manage the Mongo database (InfraV2).
    
    :param mongo_uri: The URI of the Mongo database to connect to.
    
    :method update_or_add_to_database: Update or add a company or a website content to the database.
    :method get_data_from_database: Get a company or a website content from the database.
    :method delete_data_from_database: Delete a company or a website content from the database.
    """
    def __init__(self, mongo_uri: str = os.environ["MONGO_READWRITE_PROD_URI"]):
        self._loger = create_logger("INOOPA_UTILS.DB_MANAGER.MONGO")
        self._env = os.environ.get("ENV", "dev")

        _client = MongoClient(mongo_uri)
        _db = _client[self._env]
        
        self._company_collection = _db.get_collection("company")
        self._website_content_collection = _db.get_collection("website_content")


    def update_or_add_to_database(self, data: Company) -> bool:
        """
        Update or add a company or a website content to the database.
        
        :param data: The company or website content to add or update.
        :return: True if the company or website was added, False if it was updated.
        """
        if type(data) not in [Company]:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")
        
        data_from_db = self.get_data_from_database(data)
        if data_from_db:
            raise NotImplementedError("Update is not implemented yet.")
        else:
            self._add_to_collection(data)


    def get_data_from_database(self, data: Company) -> Company | None:
        """
        Get a company or a website content from the database.
        
        :param index: The company or website index to get.
        :return: The company or website content if found, None otherwise.
        """
        if type(data) not in [Company]:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")
        
        if isinstance(data, Company):
            data_found = self._company_collection.find_one({"inoopa_id": data.inoopa_id})
            if data_found:
                self._loger.debug(f"Found data in database for company {data.inoopa_id}")
                return Company(**data_found)

        return None
    
    def delete_data_from_database(self, data: Company) -> None:
        """
        Delete a company or a website content from the database.
        
        :param data: The company or website content to delete.
        """
        if type(data) not in [Company]:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")
        
        if isinstance(data, Company):
            self._company_collection.delete_one({"inoopa_id": data.inoopa_id})
            self._loger.info(f"Deleted Company from collection {self._env} with ID: {data.inoopa_id}")
    
    def _add_to_collection(self, data: Company) -> None:
        """
        Add a company or a website content to the database.
        
        :param data: The company or website content to add.
        """
        if type(data) not in [Company]:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")
        
        if isinstance(data, Company):
            self._company_collection.insert_one(data)
            self._loger.info(f"Added Company to collection {self._env} with ID: {data.inoopa_id}")
