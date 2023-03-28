#!/usr/bin/python3
"""Module that contains functions for extracting
data from the Kobo Tool box data API
Extracting data from saved csv tables"""

import os
import pandas as pd
import requests
from etl.transform import move_csv_files


def extract_api_data(url):
    """Extracts data from given url"""
    rr = requests.get(url)
    rr_obj = rr.json()
    return pd.json_normalize(rr_obj)


def list_csv_stored():
    """Finds CSV files in my current working directory
    and returns a list of all csv files found"""
    current_wrk_dir = os.getcwd()
    csv_files = list()
    for file in os.listdir(current_wrk_dir):
        if file.endswith('.csv'):
            csv_files.append(file)
    return csv_files


def read_csv_files():
    """Reads all csv files from the directory they were
    stored. Then returns a dictionary of dataframes"""
    csv_files = list_csv_stored()
    dir_name = move_csv_files('data', csv_files)
    file_path = os.getcwd() + '/' + dir_name + '/'
    datframes = dict()
    for csv_file in csv_files:
        try:
            datframes[csv_file] = pd.read_csv(file_path + csv_file)
        except UnicodeDecodeError:
            datframes[csv_file] = pd.read_csv(file_path + csv_file, encoding="ISO-8859-1")
    return datframes, csv_files
