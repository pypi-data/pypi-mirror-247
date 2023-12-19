from dataclasses import asdict
import os
from pymongo import MongoClient

from inoopa_utils.custom_types.companies import Company
from inoopa_utils.inoopa_logging import create_logger

class DbManagerMongo:
    """
    This class is used to manage the Mongo database (InfraV2).
    
    :param mongo_uri: The URI of the Mongo database to connect to.
    
    :method update_or_add_one_to_collection: Update or add a company or a website content to the database.
    :method add_or_update_many_to_collection: Update or add a list of companies or website contents to the database.
    :method find_one_from_collection: Get a company or a website content from the database.
    :method find_many_from_collection: Get a list of companies or website contents from the database.
    :method delete_one_from_collection: Delete a company or a website content from the database.
    """
    def __init__(self, mongo_uri: str = os.environ["MONGO_READWRITE_PROD_URI"]):
        self._loger = create_logger("INOOPA_UTILS.DB_MANAGER.MONGO")
        self._env = os.environ.get("ENV", "dev")

        _client = MongoClient(mongo_uri)
        _db = _client[self._env]

        self._company_collection = _db.get_collection("company")
        self._website_content_collection = _db.get_collection("website_content")


    def update_or_add_one_to_collection(self, data: Company) -> bool:
        """
        Update or add a company or a website content to the database.
        
        :param data: The company or website content to add or update.
        :return: True if the company or website was added, False if it was updated.
        """
        if type(data) not in [Company]:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")
        
        data_from_db = self.find_one_from_collection(data)
        if data_from_db:
            raise NotImplementedError("Update is not implemented yet.")
        else:
            self._add_one_to_collection(data)

    def update_or_add_many_to_collection(self, data_list: list[Company]) -> None:
        """
        Update or add a list of companies or website contents to the database.
        
        :param data: The list of companies or website contents to add or update.
        """
        if type(data_list) not in [list] or not all(isinstance(x, Company) for x in data_list):
            raise TypeError(f"Can't update or add data to mongo. Type {type(data_list)} is not supported.")
        
        if all(isinstance(x, Company) for x in data_list):
            data_found = self.find_many_from_collection(data_list)
        else:
            raise TypeError(f"Can't update or add many data to mongo. Probably a mix of types in the list.")
        if data_found:
            raise NotImplementedError("Update is not implemented yet.")
        else:
            self._add_many_to_collection(data_list)

    def find_one_from_collection(self, data: Company) -> Company | None:
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

    def find_many_from_collection(self, data_list: list[Company]) -> list[Company] | None:
        """
        Get a list of companies or website contents from the database.

        :param data: The list of companies or website contents to get.
        :return: The list of companies or website contents if found, None otherwise.
        """
        if type(data_list) not in [list] or not all(isinstance(x, Company) for x in data_list):
            raise TypeError(f"Can't update or add data to mongo. Type {type(data_list)} is not supported.")

        if all(isinstance(x, Company) for x in data_list):
            all_ids = [x.inoopa_id for x in data_list]
            data_found = self._company_collection.find({"inoopa_id": {"$in": all_ids}})
            if data_found:
                self._loger.debug(f"Found data in database for companies {all_ids}")
                return [Company(**x) for x in data_found]
        return None

    def delete_one_from_collection(self, data: Company) -> None:
        """
        Delete a company or a website content from the database.
        
        :param data: The company or website content to delete.
        """
        if type(data) not in [Company]:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")
        
        if isinstance(data, Company):
            self._company_collection.delete_one({"inoopa_id": data.inoopa_id})
            self._loger.info(f"Deleted Company from collection {self._env} with ID: {data.inoopa_id}")

    def delete_many_from_collection(self, data_list: list[Company]) -> None:
        """
        Delete a list of companies or website contents from the database.
        
        :param data: The list of companies or website contents to delete.
        """
        if type(data_list) not in [list] or not all(isinstance(x, Company) for x in data_list):
            raise TypeError(f"Can't update or add data to mongo. Type {type(data_list)} is not supported.")
        
        if all(isinstance(x, Company) for x in data_list):
            all_ids = [x.inoopa_id for x in data_list]
            self._company_collection.delete_many({"inoopa_id": {"$in": all_ids}})
            self._loger.info(f"Deleted Companies from collection {self._env} with IDs: {all_ids}")
        else:
            raise TypeError(f"Can't update or add many data to mongo. Probably a mix of types in the list.")

    def _add_one_to_collection(self, data: Company) -> None:
        """
        Add a company or a website content to the database.

        :param data: The company or website content to add.
        """
        if type(data) not in [Company]:
            raise TypeError(f"Can't update or add data to mongo. Type {type(data)} is not supported.")

        if isinstance(data, Company):
            self._company_collection.insert_one(asdict(data))
            self._loger.info(f"Added Company to collection {self._env} with ID: {data.inoopa_id}")

    def _add_many_to_collection(self, data_list: list[Company]) -> None:
        """
        Add a list of companies or website contents to the data_listbase.
        
        :param data_list: The list of companies or website contents to add.
        """
        if type(data_list) not in [list] or not all(isinstance(x, Company) for x in data_list):
            raise TypeError(f"Can't update or add data_list to mongo. Type {type(data_list)} is not supported.")
        
        if all(isinstance(x, Company) for x in data_list):
            self._company_collection.insert_many([asdict(data) for data in data_list])
        else:
            raise TypeError(f"Can't update or add many data to mongo. Probably a mix of types in the list.")