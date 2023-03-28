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
    print("Extracting raw data from external API")
    df = extract_api_data(url)
    print("SUCCESS: Extracting of raw data from external API")
    table_names, df_dictionary = transform_dataframe(df)
    print("Creating empty tables in mysql database")
    # print(table_names, df_dictionary)
    create_empty_tables(classMap_toTables)
    print("SUCCESS: Creating empty tables in mysql database")
    print("Loading data into mysql database tables")
    load_dataframe_to_mysql(table_names, df_dictionary)
    print("SUCCESS: Loading data into mysql database tables")


if __name__ == "__main__":
    main()
