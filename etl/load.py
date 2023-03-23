#!/usr/bin/python3
"""Module contains methods used to connect dataframes
Tests for SQLAlchemy"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from models.waterscheme import WaterScheme
from models.district import District
from models.subcounty import SubCounty
from models.village import Village

# Set up database engine and session
engine = create_engine('mysql+mysqldb://nuws_dev:%s@localhost/nuws_data_db'
                       % quote('Nuws_dev_pwd@2012#')
                       , echo=False, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

"""List of classes used to map and create empty tables in mysql"""
classMap_toTables = [WaterScheme, District, SubCounty, Village]


def create_empty_tables(classes):
    """Creates empty tables in MySQL database based on a particular schema created
    from the different classes
    Args:
        classes: List of SQLAlchemy class object containing table definitions"""
    for c in classes:
        c.__table__.create(engine, checkfirst=True)
    session = Session()
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def load_dataframe_to_mysql(clean_table_names, new_dataframez):
    """Inserts data from dataframe object rows into respective tables
    created in mysql database
    Args:
        clean_table_names: list containing table names
        new_dataframez: dictionary containing dataframe objects to respective
        clean_table_names"""
    for table_name in clean_table_names:
        df = new_dataframez[table_name]
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
