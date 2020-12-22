"""
 * Project Name: RippedWebServer
 * user Name: db.py
 * Programmer: Kai Prince
 * Date: Mon, Dec 12, 2020
 * Description: This user contains DB service functions for the auth app.
"""

from bson.objectid import ObjectId
from pymongo import MongoClient

from db.repositories import IUsersRepository


class UsersMongoRepository(IUsersRepository):
    db_name = "auth"
    collection_name = "users"

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
        """ Consumes an ID and produces user details. """
        record = self.collection.find_one({"_id": ObjectId(obj_id)})
        record = self._conform(record)

        return record

    def search(self, predicate):
        all_items = self.index()
        all_items = [self._conform(x) for x in all_items]
        search_results = [x for x in all_items if predicate(x)]

        return search_results

    def create(self, username, password, permissions):
        # TODO validate permissions
        result = self.collection.insert_one(
            {"username": username, "password": password, "permissions": permissions}
        )

        return result

    def edit(self, user_id, username, password, permissions):
        # TODO validate permissions
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "username": username,
                "password": password,
                "permissions": permissions,
            },
        )

        return result

    def delete(self, user_id):
        result = self.collection.delete_one({"_id": ObjectId(user_id)})

        return result

    def _conform(self, record):
        """
        * Function Name: _conform
        * Description: This function is used to convert a MongoDb record
        *  into a standard JSON record.
        * Parameters:
            MongoDb record {"_id": ObjectId("")}
        * Returns:
            dict {"user_id": int}
        """
        if record is None:
            return record

        result = {**record, "user_id": str(record["_id"])}
        result.pop("_id", None)

        return result
