#!/usr/bin/python3
"""This module is the basemodel to be inherited by other
class models to set up the table schemas for the database
"""
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import uuid
import etl.models

time = '%Y-%m-%dT%H:%M:%S.%f'
Base = declarative_base()


class BaseModel:
    """Base Model to be inherited by all other class models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(), nullable=True, default=datetime.now,
                        onupdate=datetime.now)

    def __init__(self, **kwargs):
        if kwargs is not None:
            for key, val in kwargs.items():
                if key != "__class__":
                    if key in ['created_at', 'updated_at']:
                        if type(val) is str:
                            val = datetime.strftime(val, time)
                    setattr(self, key, val)
        if len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.strftime(datetime.today(), time)
            self.updated_at = datetime.strftime(datetime.today(), time)

    def __str__(self):
        """Returns string representation of created objects"""
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def to_dict(self):
        """Converts object to dictionary format"""
        dictionary = self.__dict__.copy()
        dictionary.update({'__class__': self.__class__.__name__})
        if "created_at" in dictionary and dictionary['created_at'] is not None:
            dictionary['created_at'] = dictionary['created_at'].strftime(time)
        if 'updated_at' in dictionary and dictionary['updated_at'] is not None:
            dictionary['updated_at'] = dictionary['updated_at'].strftime(time)
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def save(self):
        """Saves current object to the database"""
        etl.models.storage.new(self)
        etl.models.storage.save()

    def delete(self):
        """Deletes current object from the database"""
        etl.models.storage.delete(self)
