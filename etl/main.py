#!/usr/bin/python3
"""Main entry point for the data pipeline service application"""
import sys
from extract import extract_api_data
from extract import transform


def main():
    """Main entry point into pipeline app
    include later validation to ensure one parameter is parsed"""
    baseUrl = sys.argv[1]
    url = baseUrl + '.json'
    df = extract_api_data(url)
    pds = transform(df)
    print(pds)


if __name__ == "__main__":
    main()
