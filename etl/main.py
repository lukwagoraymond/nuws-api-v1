#!/usr/bin/python3
"""Main entry point for the data pipeline service application"""
import sys
from etl.extract import extract_api_data
from etl.transform import transform_dataframe
from etl.models.load import create_empty_tables, load_dataframe_to_mysql, classMap_toTables


def main():
    """Main entry point into pipeline app
    include exception handling to ensure url is included in main.py"""
    baseUrl = sys.argv[1]
    url = baseUrl + '.json'
    df = extract_api_data(url)
    table_names, df_dict = transform_dataframe(df)
    create_empty_tables(classMap_toTables)
    load_dataframe_to_mysql(table_names, df_dict)


if __name__ == "__main__":
    main()
