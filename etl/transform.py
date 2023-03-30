#!/usr/bin/python3
"""Module containing functions to support data
transformations of the fetched data
"""

import pandas as pd
import os
import uuid
import loguru
from etl.config_files import config

"""command to suppress Setting With Copy Warning when 
updating columns with new data
"""
pd.set_option('mode.chained_assignment', None)
logger = loguru.logger


def transform_dataframe(df):
    """Takes up pandas dataframe; removes unwanted columns
    creates different pd objects based on data model and returns dictionaries"""
    transform_columns(df, config.coldict, config.columns_to_drop)
    new_df = insert_items(df, config.coladd)
    new_df = new_df.astype(config.col_datatypes)
    new_df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    dd = save_tables(new_df)
    logger.success("Imported Pandas Dataframe columns transformed as expected")
    table_names, df_dictionary = clean_import_tables(dd)
    return table_names, df_dictionary


def transform_columns(df, coldict, collist=None):
    """Remove columns & rename column names based on data model names
    Args: dataframe object
    coldict dictionary of new columns
    collist list of columns to remove"""
    try:
        if collist is not None:
            df.drop(collist, inplace=True, axis=1)
        df.rename(columns={k: v for k, v in coldict.items()}, inplace=True)
    except Exception as e:
        logger.error(f"ERROR: The columns were not transformed as expected with error: {e}")


def insert_items(df, coladd):
    """Inserts new columns to dataframe object
    And fills columns with corresponding values from
    list argument"""
    df2 = df.reindex(df.columns.tolist() + coladd, axis=1)
    for i in coladd:
        if i == 'dis_id':
            df2[i] = df['district']
            df2 = assign_uuid(df2, i, config.uuids_dist)
        elif i == 'sc_id':
            df2[i] = df['subCounty']
            df2 = assign_uuid(df2, i, config.uuids_subc)
        elif i == 'vil_id':
            df2[i] = df2[i].apply(lambda v: str(uuid.uuid4()))
    return df2


def assign_uuid(df, column_name, value_dict):
    """Assigns a UUID to a row label under a column in a pandas Dataframe
    if the row table in another column equals a particular entry.
    Parameters:
        df (pandas.DataFrame): The input Dataframe.
        column_name (str): The name of the column to modify
        value_dict (str): The value to use for th
    Returns:
        pandas.DataFrame: The modified DataFrame"""
    for key, value in value_dict.items():
        df[column_name] = df[column_name].replace(key, value)
    return df


def save_tables(df):
    """Saves the split df objects into seperate tables
    as per the data model - Optimise later."""
    # Splits the tables
    waterScheme = df[['name', 'id', 'dis_id', 'sc_id', 'energySource', 'designYield',
                      'yearEstablish', 'created_at']]
    transform_columns(waterScheme, coldict={'dis_id': 'district_id',
                                            'sc_id': 'sub_county_id'}, collist=None)
    waterScheme.drop_duplicates(subset=['id'], keep='first', inplace=True)

    district = df[['district', 'created_at', 'dis_id']]
    transform_columns(district, coldict={'district': 'name',
                                         'dis_id': 'id'}, collist=None)
    district.drop_duplicates(subset=['id'], keep='first', inplace=True)

    subCounty = df[['subCounty', 'created_at', 'dis_id', 'sc_id']]
    transform_columns(subCounty, coldict={'subCounty': 'name',
                                          'dis_id': 'district_id',
                                          'sc_id': 'id'}, collist=None)
    subCounty.drop_duplicates(subset=['id'], keep='first', inplace=True)

    village = df[['village', 'created_at', 'sc_id', 'vil_id', 'dis_id']]
    transform_columns(village, coldict={'village': 'name',
                                        'sc_id': 'sub_county_id',
                                        'vil_id': 'id',
                                        'dis_id': 'district_id'}, collist=None)
    village.drop_duplicates(subset=['id'], keep='first', inplace=True)
    dfs = {
        'district': district,
        'subCounty': subCounty,
        'village': village,
        'waterScheme': waterScheme
    }
    """write_df_to_file(subCounty, 'subCounty', subCounty.columns)
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
    try:
        clean_table_names = list()
        new_dataframez = dict()
        if type(dataframez) is dict:
            csv_list = list()
            for key in dataframez.keys():
                csv_list.append(key)
            csv_files = csv_list
        else:
            csv_files = csv_files
        for k in csv_files:
            dataframe = dataframez[k]
            # Clean table names
            clean_tbl_name = k.lower().replace(" ", "_").replace("?", "") \
                .replace("-", "_").replace(r"/", "_").replace("\\", "_") \
                .replace("%", "").replace(")", "").replace(r"(", "").replace("$", "")
            if clean_tbl_name.endswith('.csv'):
                clean_tbl_name = clean_tbl_name[:-4]
            else:
                clean_tbl_name
            clean_table_names.append(clean_tbl_name)
            # Clean dataframe columns
            dataframe.columns = [x.lower().replace(" ", "_").replace("?", "")
                                 .replace("-", "_").replace(r"/", "_").replace("\\", "_")
                                 .replace("%", "").replace(")", "").replace(r"(", "")
                                 .replace("$", "") for x in dataframe.columns]
            new_dataframez[clean_tbl_name] = dataframe
        logger.success(f"Dataframes {[x for x in clean_table_names]} were cleaned well")
        return clean_table_names, new_dataframez
    except Exception as e:
        logger.error(f"Dataframes {clean_table_names} were not cleaned well with error: {e}")
