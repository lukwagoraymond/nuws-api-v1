#!/usr/bin/python3
"""Water Scheme Module for NUWS API Project"""
from etl.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, Float
from datetime import datetime
from sqlalchemy.orm import relationship


class WaterScheme(BaseModel, Base):
    """Class for the water scheme table in storage"""
    __tablename__ = 'waterscheme'
    name = Column(String(255), nullable=False)
    energySource = Column(String(255), nullable=False)
    constructionYear = Column(DateTime(), nullable=True, default=datetime.date)
    designYield = Column(Float(), nullable=False)
    district = relationship("District", backref='waterscheme', cascade="all, delete")

    def __init__(self, **kwargs):
        """Initialises water scheme object attributes"""
        super().__init__(**kwargs)
