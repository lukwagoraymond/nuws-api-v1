#!/usr/bin/python3
"""District Module for NUWS API Project"""
from etl.models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class District(BaseModel, Base):
    """Class for District Table in Database"""
    __tablename__ = 'district'
    name = Column(String(255), nullable=False)
    subCounty_id = relationship("SubCounty", backref='dist_id')
    district_id = relationship("WaterScheme", backref='dis_id')
    village_1 = relationship("Village", backref='dist_id', cascade='all, delete')
