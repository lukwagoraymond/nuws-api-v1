#!/usr/bin/python3
"""Sub County Module for NUWS API Project"""
from etl.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class SubCounty(BaseModel, Base):
    """Class for Sub County Table in Database"""
    __tablename__ = 'subcounty'
    name = Column(String(255), nullable=False)
    district_id = Column(String(255), ForeignKey('district.id'), nullable=False)
    village = relationship("Village", backref='subcounty', cascade='all, delete')
