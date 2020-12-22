"""
 * Project Name: RippedWebServer
 * File Name: factories.py
 * Programmer: Kai Prince
 * Date: Sun, Dec 13, 2020
 * Description: This file contains factory functions for all repository
 *  implementations.
"""

import sqlite3

from flask import current_app
from pymongo import MongoClient

from db.repositories.mongo import FilesMongoRepository
from db.repositories.sql import FilesSqlRepository


def get_sql_db():

    connection_string = current_app.config["DATABASE"]
    return sqlite3.connect(connection_string, detect_types=sqlite3.PARSE_DECLTYPES)


def get_mongo_db():
    username = current_app.config["MONGO_USERNAME"]
    password = current_app.config["MONGO_PASSWORD"]
    dbname = current_app.config["MONGO_DBNAME"]
    mongo_uri = (
        str(current_app.config["DATABASE"])
        .replace("{username}", username)
        .replace("{password}", password)
        .replace("{dbname}", dbname)
    )

    db = MongoClient(mongo_uri)
    return db


def make_files_sql_repo():
    db = get_sql_db()
    return FilesSqlRepository(db)


def make_files_mongo_repo():
    db = get_mongo_db()
    return FilesMongoRepository(db)
