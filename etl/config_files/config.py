#!/usr/bin/python3
"""Module contains configuration information
needed to access mysql server,
Needed information to transform original dataframe object"""

import os

"""Information to use to access mysql server
"""
DB_DETAILS = {
    'dev': {
            'DB_TYPE': 'mysql',
            'DB_HOST': 'localhost',
            'DB_NAME': 'nuws_data_db',
            'DB_USER': 'nuws_dev',
            'DB_PASS': 'Nuws_dev_pwd@2012#'
    }
}
# os.environ.get('TARGET_DB_PASS')

"""List containing columns to drop from fetched api data
"""
columns_to_drop = ["_id", "start", "__version__", "meta/instanceID",
                   "_xform_id_string", '_attachments', '_status',
                   '_geolocation', '_submission_time', '_tags',
                   '_notes', '_submitted_by', 'formhub/uuid']

"""Dictionary containing columns names to change from fetched api data
Format is:
{old_column_name: new_column_name}
"""
coldict = {'schemeName': 'name', '_uuid': 'id', 'end': 'created_at'}

"""Additional columns to be added to the fetched api data"""
coladd = ['dis_id', 'sc_id', 'vil_id']

"""Replacement dictionary that maps pandas dtypes to new desired dtypes"""
col_datatypes = {'created_at': 'datetime64[ns]', 'name': 'string',
                 'yearEstablish': 'datetime64[ns]', 'energySource': 'string',
                 'designYield': 'float', 'district': 'string',
                 'subCounty': 'string', 'village': 'string',
                 'id': 'string', 'dis_id': 'string', 'sc_id': 'string',
                 'vil_id': 'string'}

"""Dictionary of uuids to be assigned to particular row labels under district, sub-county
and village id columns"""
uuids_dist = {'yumbe': 'c3213dbb-78fb-4ec7-8424-ff639639d913',
              'terego': '9cfc710c-3997-42c5-a314-7be239e11c43',
              'madi': '00d770d6-e0f4-4ef0-8ef8-d34942578893',
              'arua': '72522cfe-a301-47f5-b935-6602761730f8'}
uuids_subc = {'ariwa': '6e52f9e9-720f-4187-9cf9-bcc6a4fce1b2',
              'kululu': '39df2ad7-1940-4671-83e9-94221c4c68c7',
              'romogi': '61c1e6a6-0523-44f9-b4f6-14d322abc68b',
              'odravu': '211462b1-6be8-4f18-9374-56192a53803c',
              'kochi': 'ce37f5c5-1c6d-4e9b-9b7a-8d97254a4ac2',
              'uriama': '7957715c-e5e4-48e0-80f8-5e1684c9cfba',
              'odupi': 'cdf007b5-0a84-4fd2-8db3-e1a765301c26',
              'omugo': '0064f92b-0c8a-43df-be17-a51b18bac449',
              'rigbo': '1f14b5fa-3edd-4fa2-8899-101d6e0686d0',
              'vuura': '54db20f5-bf50-4a2a-95e2-45ce9fb18136',
              'nvaara': '843c6cfc-782f-49b9-a942-7d2800c53979',
              'oduparaka': '32cc0241-bbd3-4032-9b2b-ec18c9c5648c'}
