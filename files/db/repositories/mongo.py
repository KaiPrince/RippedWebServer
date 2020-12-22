"""
 * Project Name: RippedWebServer
 * File Name: db.py
 * Programmer: Kai Prince
 * Date: Mon, Nov 30, 2020
 * Description: This file contains DB service functions for the files app.
"""

from db.repositories import IFilesRepository
from pymongo import MongoClient
from bson.objectid import ObjectId


class FilesMongoRepository(IFilesRepository):
    db_name = "files"
    collection_name = "files"

    def __init__(self, db: MongoClient):
        self.db_instance: MongoClient = db
        self.db = db.get_database(self.db_name)
        self.collection = self.db.get_collection(self.collection_name)

    def index(self):
        records = self.collection.find()
        results = [self._add_file_id_field(x) for x in records]

        return results

    def get_by_id(self, obj_id):
        """ Consumes an ID and produces file details. """
        record = self.collection.find_one({"_id": ObjectId(obj_id)})
        record = self._add_file_id_field(record)

        return record

    def search(self, predicate):
        all_items = self.index()
        search_results = [x for x in all_items if predicate(x)]

        return search_results

    def create(self, file_name, user_id, file_path):
        result = self.collection.insert_one(
            {
                "file_name": file_name,
                "user_id": user_id,
                "file_path": file_path,
            }
        )

        return result

    def edit(self, file_id, file_name, user_id, file_path):
        result = self.collection.update_one(
            {"_id": file_id},
            {
                "file_name": file_name,
                "user_id": user_id,
                "file_path": file_path,
            },
        )

        return result

    def delete(self, file_id):
        result = self.collection.delete_one({"_id": file_id})

        return result

    def _add_file_id_field(self, record):
        if record is None:
            return record

        result = {**record, "file_id": str(record["_id"])}
        result.update({"_id": None})

        return result
