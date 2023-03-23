#!/usr/bin/python3
"""Village Module for NUWS API Project"""
from etl.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Village(BaseModel, Base):
    """Class for Village Table in Database"""
    __tablename__ = 'village'
    name = Column(String(255), nullable=False)
    subcounty_id = Column(String(255), ForeignKey('subcounty.id'), nullable=False)
