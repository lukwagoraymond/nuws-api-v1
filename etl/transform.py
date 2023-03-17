#!/usr/bin/python3
"""Module containing functions to support data
transformations"""
import uuid


def transform_columns(df, coldict, collist):
    """Remove columns & rename column names based on data model names
    Args: dataframe object
    coldict dictionary of new columns
    collist list of columns to remove"""
    df.drop(collist, inplace=True, axis=1)
    df.rename(columns={k: v for k, v in coldict.items()},
              inplace=True)


def insert_items(df, coladd):
    """Inserts new columns to dataframe object
    And fills columns with corresponding values from
    list argument"""
    df2 = df.reindex(df.columns.tolist() + coladd, axis=1)
    for i in coladd:
        df2[i].fillna(str(uuid.uuid4()), inplace=True)
    return df2
