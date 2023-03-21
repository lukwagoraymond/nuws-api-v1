#!/usr/bin/python3
"""This module is the basemodel to be inherited by other
class models to set up the table schemas for the database
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """Base Model to be inherited by all other class models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(), nullable=True, default=datetime.now,
                        onupdate=datetime.now)

    def __str__(self):
        """Returns string representation of created objects"""
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def to_dict(self):
        """Converts object to dictionary format"""
        dictionary = dict()
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': self.__class__.__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.created_at.isoformat()
        return dictionary

    def save(self):
        """Saves current object to the database"""
        pass

    def delete(self):
        """Deletes current object from the database"""
        pass

