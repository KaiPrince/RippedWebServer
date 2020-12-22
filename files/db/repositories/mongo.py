"""
 * Project Name: RippedWebServer
 * File Name: db.py
 * Programmer: Kai Prince
 * Date: Mon, Nov 30, 2020
 * Description: This file contains DB service functions for the files app.
"""

from datetime import datetime

from bson.objectid import ObjectId
from pymongo import MongoClient

from db.repositories import IFilesRepository


class FilesMongoRepository(IFilesRepository):
    db_name = "files"
    collection_name = "files"

    def __init__(self, db: MongoClient):
        self.db_instance: MongoClient = db
        self.db = db.get_database(self.db_name)
        self.collection = self.db.get_collection(self.collection_name)

    def __del__(self):
        self.db_instance.close()

    def index(self):
        records = self.collection.find()
        results = [self._conform(x) for x in records]

        return results

    def get_by_id(self, obj_id):
        """ Consumes an ID and produces file details. """
        record = self.collection.find_one({"_id": ObjectId(obj_id)})
        record = self._conform(record)

        return record

    def search(self, predicate):
        all_items = self.index()
        all_items = [self._conform(x) for x in all_items]
        search_results = [x for x in all_items if predicate(x)]

        return search_results

    def create(self, file_name, user_id, file_path):
        result = self.collection.insert_one(
            {
                "file_name": file_name,
                "user_id": user_id,
                "file_path": file_path,
                "uploaded": datetime.now(),
            }
        )

        return result

    def edit(self, file_id, file_name, user_id, file_path):
        result = self.collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "file_name": file_name,
                "user_id": user_id,
                "file_path": file_path,
            },
        )

        return result

    def delete(self, file_id):
        result = self.collection.delete_one({"_id": ObjectId(file_id)})

        return result

    def _conform(self, record):
        """
        * Function Name: _conform
        * Description: This function is used to convert a MongoDb record
        *  into a standard JSON record.
        * Parameters:
            MongoDb record {"_id": ObjectId("")}
        * Returns:
            dict {"file_id": int}
        """
        if record is None:
            return record

        result = {**record, "file_id": str(record["_id"])}
        result.pop("_id", None)

        return result
