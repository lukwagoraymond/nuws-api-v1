#!/usr/bin/python3
"""This module instantiates an object of DBStorage
once automatically whenever it is imported into another
module"""
from etl.models.engine.db_storage import DBStorage
storage = DBStorage()
storage.reload_api()
