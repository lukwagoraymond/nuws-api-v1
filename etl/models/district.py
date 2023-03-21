#!/usr/bin/python3
"""District Module for NUWS API Project"""
from base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class District(BaseModel, Base):
    """Class for District Table in Database"""
    __tablename__ = 'district'
    name = Column(String(255), nullable=False)
    scheme_id = Column(String(255), ForeignKey('waterscheme.id'), nullable=False)
    subCounty = relationship("SubCounty", backref='district', cascade='all, delete')
