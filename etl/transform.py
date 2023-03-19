#!/usr/bin/python3
"""Module containing functions to support data
transformations of the fetched data
"""

import pandas as pd
import os
import uuid
from config_files import config

"""command to suppress Setting With Copy Warning when 
updating columns with new data
"""
pd.set_option('mode.chained_assignment', None)


def transform_dataframe(df):
    """Takes up pandas dataframe; removes unwanted columns
    creates different pd objects based on data model and returns dictionaries"""
    transform_columns(df, config.coldict, config.columns_to_drop)
    new_df = insert_items(df, config.coladd)
    new_df = new_df.astype(config.col_datatypes)
    dd = save_tables(new_df)
    dd2 = clean_import_tables(dd)
    return dd2


def transform_columns(df, coldict, collist=None):
    """Remove columns & rename column names based on data model names
    Args: dataframe object
    coldict dictionary of new columns
    collist list of columns to remove"""
    if collist is not None:
        df.drop(collist, inplace=True, axis=1)
    df.rename(columns={k: v for k, v in coldict.items()},
              inplace=True)


def insert_items(df, coladd):
    """Inserts new columns to dataframe object
    And fills columns with corresponding values from
    list argument"""
    df2 = df.reindex(df.columns.tolist() + coladd, axis=1)
    for i in coladd:
        df2[i] = df2[i].apply(lambda v: str(uuid.uuid4()))
    return df2


def save_tables(df):
    """Saves the split df objects into seperate tables
    as per the data model - Optimise later."""
    # Splits the tables
    waterScheme = df[['name', 'id', 'energySource', 'designYield',
                      'yearEstablish', 'created_at']]

    district = df[['district', 'id', 'created_at', 'dis_id']]
    transform_columns(district, coldict={'district': 'name',
                                         'id': 'scheme_id',
                                         'dis_id': 'id'}, collist=None)

    subCounty = df[['subCounty', 'created_at', 'dis_id', 'sc_id']]
    transform_columns(subCounty, coldict={'subCounty': 'name',
                                          'dis_id': 'district_id',
                                          'sc_id': 'id'}, collist=None)

    village = df[['village', 'created_at', 'sc_id', 'vil_id']]
    transform_columns(village, coldict={'village': 'name',
                                        'sc_id': 'sub-county_id',
                                        'vil_id': 'id'}, collist=None)
    dfs = {
        'waterScheme': waterScheme,
        'district': district,
        'subCounty': subCounty,
        'village': village
    }
    """
    write_df_to_file(waterScheme, 'waterScheme', waterScheme.columns)
    write_df_to_file(district, 'district', district.columns)
    write_df_to_file(subCounty, 'subCounty', subCounty.columns)
    write_df_to_file(village, 'village', village.columns)"""
    return dfs


def write_df_to_file(df, filename, columns):
    """Takes in df and filename & saves to csv"""
    file_path = f'{filename}.csv'
    df.to_csv(file_path, header=columns, index=False, mode='a')


def move_csv_files(dir_name, csv_files):
    """Function creates a new directory name in the current
    working directory and then moves all csv files to that
    directory"""
    try:
        mkdir_cmd = f'mkdir -p {dir_name}'
        os.system(mkdir_cmd)
    except OSError:
        raise "The folder already exists"

    for csv in csv_files:
        cp_cmd = f"cp '{csv}' {dir_name}"
        os.system(cp_cmd)
    return dir_name


def clean_import_tables(dataframez, csv_files=None):
    """ Cleans imported dataframes. if function used after read_csv_files then
     use csv_file list return else create a list from dictionary from keys of
     generated dfs under save_tables function"""
    if type(dataframez) is dict:
        csv_list = list()
        for key in dataframez.keys():
            csv_list.append(key)
        csv_files = csv_list
    else:
        csv_files = csv_files
    for k in csv_files:
        dataframe = dataframez[k]
        clean_tbl_name = k.lower().replace(" ", "_").replace("?", "") \
            .replace("-", "_").replace(r"/", "_").replace("\\", "_") \
            .replace("%", "").replace(")", "").replace(r"(", "").replace("$", "")
        if clean_tbl_name.endswith('.csv'):
            clean_tbl_name = clean_tbl_name[:-4]
        dataframe.columns = [x.lower().replace(" ", "_").replace("?", "")
                             .replace("-", "_").replace(r"/", "_").replace("\\", "_")
                             .replace("%", "").replace(")", "").replace(r"(", "")
                             .replace("$", "") for x in dataframe.columns]
    return clean_tbl_name, dataframe
