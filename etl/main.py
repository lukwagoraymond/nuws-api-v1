#!/usr/bin/python3
"""Main entry point for the data pipeline service application"""
import sys
from extract import extract_api_data
from transform import transform_dataframe


def main():
    """Main entry point into pipeline app
    include exception handling to ensure url is included in main.py"""
    baseUrl = sys.argv[1]
    url = baseUrl + '.json'
    df = extract_api_data(url)
    pds = transform_dataframe(df)
    print(pds)


if __name__ == "__main__":
    main()
