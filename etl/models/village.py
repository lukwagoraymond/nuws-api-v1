#!/usr/bin/python3
"""Village Module for NUWS API Project"""
from etl.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Village(BaseModel, Base):
    """Class for Village Table in Database"""
    __tablename__ = 'village'
    name = Column(String(255), nullable=False)
    sub_county_id = Column(String(60), ForeignKey('subcounty.id'), nullable=False)
    district_id = Column(String(60), ForeignKey('district.id'), nullable=False)
