#!/usr/bin/python3
"""Contains Storage Engine Model to support connection and
CRUD operations between the database and objects created"""

from etl.models.base_model import Base
from etl.config_files.config import DB_DETAILS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from urllib.parse import quote


class DBStorage:
    """This is the Database Storage Engine Class"""
    __engine = None
    __session = None

    def __init__(self):
        """Automatically instantiates whenever class is called"""
        MYSQL_DB = DB_DETAILS['dev']
        self.__engine = create_engine('mysql+mysqldb://nuws_dev:%s@localhost/nuws_data_db'
                                      % quote('Nuws_dev_pwd@2012#')
                                      , echo=False, pool_pre_ping=True)

    def new(self, obj):
        """Adds a new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes in the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload_pandas(self, obj):
        """Creates tables based on classes provided in a list"""
        obj.create(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def reload_api(self):
        """Creates tables in the database based on the class models created.
        Creates the current database session from created engine using
        sessionmaker"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def rollback_changes(self):
        """Rolls back changes to previous session before changes"""
        self.__session.rollback()

    def close(self):
        """Calls SQLAlchemy remove() method on the private session above"""
        self.__session.remove()
