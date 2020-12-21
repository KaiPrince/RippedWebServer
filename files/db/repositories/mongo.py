"""
 * Project Name: RippedWebServer
 * File Name: db.py
 * Programmer: Kai Prince
 * Date: Mon, Nov 30, 2020
 * Description: This file contains DB service functions for the files app.
"""

from db.repositories import IFilesRepository
from pymongo import MongoClient


class FilesMongoRepository(IFilesRepository):
    db_name = "files"
    collection_name = "files"

    def __init__(self, db: MongoClient):
        self.db_instance: MongoClient = db
        self.db = db.get_database(self.db_name)
        self.collection = self.db.get_collection(self.collection_name)

    def index(self):
        all_items = self.collection.find()
        return all_items

    def get_by_id(self, obj_id):
        """ Consumes an ID and produces file details. """
        return self.collection.find_one({"_id": obj_id})

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
            {"file_id": file_id},
            {
                "file_name": file_name,
                "user_id": user_id,
                "file_path": file_path,
            },
        )

        return result

    def delete(self, file_id):
        result = self.collection.delete_one({"file_id": file_id})

        return result
