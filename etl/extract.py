#!/usr/bin/python3
"""Module that contains functions for extracting
data from the Kobo Tool box data API"""

import requests
import pandas as pd
from transform import *

# string path to the original JSON file containing data extract from API
__file_path = "file.json"
pd.set_option('mode.chained_assignment', None)


def extract_api_data(url):
    """Extracts data from given url"""
    rr = requests.get(url)
    rr_obj = rr.json()
    return pd.json_normalize(rr_obj)


def transform(df):
    """Takes up pandas dataframe; removes unwanted columns
    creates different pd objects based on data model and returns dictionaries"""
    columns_to_drop = ["_id", "start", "__version__", "meta/instanceID",
                       "_xform_id_string", '_attachments', '_status',
                       '_geolocation', '_submission_time', '_tags',
                       '_notes', '_submitted_by', 'formhub/uuid']
    coldict = {'schemeName': 'name', '_uuid': 'id', 'end': 'created_at'}
    coladd = ['dis_id', 'sc_id', 'vil_id']
    transform_columns(df, coldict, columns_to_drop)
    new_df = insert_items(df, coladd)
    fin_dic = save_tables(new_df)

    # Split the dataframes into different tables per data model
    # Return concatenated list of dictionaries for each table in one dictionary
    # Convert different dataframes into dict based on particular format.
    # employ rename function here

    return fin_dic
