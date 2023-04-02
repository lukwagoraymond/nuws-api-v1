#!/usr/bin/python3
"""Module contains methods used to connect dataframes
Tests for SQLAlchemy"""
import os
import pandas as pd
from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from etl.models.waterscheme import WaterScheme
from etl.models.district import District
from etl.models.subcounty import SubCounty
from etl.models.village import Village

# Set up database engine and session
DB_HOST = os.environ.get("DB_HOST", 'localhost')
DB_NAME = os.environ.get("DB_NAME", 'nuws_data_db')
DB_USER = os.environ.get("DB_USER", 'nuws_dev')
DB_PASS = os.environ.get("DB_PASS", 'Nuws_dev_pwd@2012#')
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                       format(DB_USER, quote(DB_PASS),
                              DB_HOST, DB_NAME),
                       echo=False, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

"""List of classes used to map and create empty tables in mysql"""
classMap_toTables = [WaterScheme, District, SubCounty, Village]


def create_empty_tables(classes):
    """Creates empty tables in MySQL database based on a particular schema created
    from the different classes
    Args:
        classes: List of SQLAlchemy class object containing table definitions"""
    try:
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
        logger.success("SUCCESS: Tables in mysql database created")
    except Exception as e:
        logger.error(f"ERROR: Tables were not created as error: {e}")


def check_and_insert(df, table_name):
    """Checks if a row value in a pandas dataframe is present in a MYSQL table using
    SQLAlchemy, and if it is not present, inserts the row value using the to_sql
    method of Pandas
    :param df: The Pandas dataframe to check and insert into MYSQL
    :param table_name: The name of the MYSQL table to check and insert into"""
    # Escape special characters '-' in the id column of the dataframe
    df['id'] = df['id'].apply(quote)
    # Query the MYSQL table to check if the IDs are already present
    existing_ids = pd.read_sql_query(text(f"SELECT id FROM {table_name}"),
                                     engine.connect())['id'].tolist()
    # Filter the Dataframe to only include rows with IDs that are not already present in MYSQL table
    df_to_insert = df[~df['id'].isin(existing_ids)]
    return df_to_insert


def load_dataframe_to_mysql(clean_table_names, new_dataframez):
    """Inserts data from dataframe object rows into respective tables
    created in mysql database
    Args:
        clean_table_names: list containing table names
        new_dataframez: dictionary containing dataframe objects to respective
        clean_table_names"""
    for table_name in clean_table_names:
        df = new_dataframez[table_name]
        df_to_insert = check_and_insert(df, table_name)
        if not df_to_insert.empty:
            df_to_insert.to_sql(table_name, con=engine, if_exists='append', index=False)
    logger.success("SUCCESS: Loaded data into mysql database tables")
