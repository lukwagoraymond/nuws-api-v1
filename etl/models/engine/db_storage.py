#!/usr/bin/python3
"""Contains Storage Engine Model to support connection and
CRUD operations between the database and objects created"""

from etl.models.base_model import Base
from etl.models.waterscheme import WaterScheme
from etl.models.district import District
from etl.models.subcounty import SubCounty
from etl.models.village import Village
from etl.config_files.config import DB_DETAILS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from urllib.parse import quote

classes = {"WaterScheme": WaterScheme, "District": District,
           "SubCounty": SubCounty, "Village": Village}


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
            self.save()

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
        session-maker"""
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

    def all(self, cls=None):
        """Query MySQL database and return object containing
        data of all row data stored in form of a list of that
        class"""
        new_dict = dict()
        if cls is not None:
            objs = self.__session.query(classes[cls])
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        for c in classes.values():
            objs = self.__session.query(c)
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return new_dict

    def get_obj(self, cls, id):
        """Retrieves an object based on the class name and id"""
        if cls and id:
            fetch = f'{cls}.{id}'
            all_objs = self.all(cls)
            return all_objs.get_obj(fetch)
        return None

    def count(self, cls=None):
        """Returns the number of objects in DB storage matching given class
        else returns all objects if no class is passed"""
        if cls:
            return len(self.all(cls))
        return len(self.all())
