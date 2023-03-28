#!/usr/bin/python3
"""Water Scheme Module for NUWS API Project"""
from etl.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from datetime import datetime


class WaterScheme(BaseModel, Base):
    """Class for the water scheme table in storage"""
    __tablename__ = 'waterscheme'
    name = Column(String(255), nullable=False)
    energysource = Column(String(255), nullable=False)
    yearestablish = Column(DateTime(), nullable=True, default=datetime.date)
    designyield = Column(Float(), nullable=False)
    district_id = Column(String(60), ForeignKey('district.id'))
    sub_county_id = Column(String(60), ForeignKey('subcounty.id'))

    def __init__(self, **kwargs):
        """Initialises water scheme object attributes"""
        super().__init__(**kwargs)
