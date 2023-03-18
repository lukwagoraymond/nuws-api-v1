#!/usr/bin/python3
"""Module containing functions to support data
transformations"""
import uuid
import os


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

    write_df_to_file(waterScheme, 'waterScheme')
    write_df_to_file(district, 'district')
    write_df_to_file(subCounty, 'subCounty')
    write_df_to_file(village, 'village')


def write_df_to_file(df, filename):
    """Takes in df and filename & saves to csv"""
    file_path = f'{filename}.csv'
    df.to_csv(file_path, index=False, sep=':')
