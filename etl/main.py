#!/usr/bin/python3
"""Main entry point for the data pipeline service application"""
import sys
import os
from loguru import logger
from etl.extract import extract_api_data
from etl.transform import transform_dataframe
from etl.models.load import create_empty_tables, load_dataframe_to_mysql, classMap_toTables

# Set Custom Logger
logger.remove()
log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'etl.log')
logger.add(sys.stdout, colorize=True, format="<g>{time:YYYY-MM-DD at HH:mm:ss}</> |"
                                             " {level} | <b>{name}:{module}:{line}</> |"
                                             " {process} >>> <b><lvl>{message}</></>")


def main():
    """Main entry point into pipeline app
    include exception handling to ensure url is included in main.py"""
    try:
        baseUrl = sys.argv[1]
        url = baseUrl + '.json'
        logger.info("Extracting raw data from Kobo-toolbox")
    except IndexError as e:
        logger.error(f"ERROR: Please provide an argument to main module: See error {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred with error {e}")
        sys.exit(1)

    df = extract_api_data(url)
    table_names, df_dictionary = transform_dataframe(df)
    if not table_names or not df_dictionary:
        logger.error(f"Either {table_names} or {df_dictionary} is empty")
        sys.exit(1)
    else:
        logger.info("Creating empty tables in 'nuws_data_db' database")
    create_empty_tables(classMap_toTables)
    logger.info("Loading data into mysql database tables")
    load_dataframe_to_mysql(table_names, df_dictionary)
    sys.exit(0)


if __name__ == "__main__":
    main()
