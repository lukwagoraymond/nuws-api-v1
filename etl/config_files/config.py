#!/usr/bin/python3
"""Module contains configuration information
needed to access mysql server,
Needed information to transform original dataframe object"""

import os

"""Information to use to access mysql server
"""
DB_DETAILS = {
    'dev': {
        'TARGET_DB': {
            'DB_TYPE': 'mysql',
            'DB_HOST': '127.0.0.1',
            'DB_NAME': 'nuws_data',
            'DB_USER': os.environ.get('TARGET_DB_USER'),
            'DB_PASS': os.environ.get('TARGET_DB_PASS')
        }
    }
}

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

col_datatypes = {'created_at': 'datetime64[ns]', 'name': 'string',
                 'yearEstablish': 'datetime64[ns]', 'energySource': 'string',
                 'designYield': 'float', 'district': 'string',
                 'subCounty': 'string', 'village': 'string',
                 'id': 'string', 'dis_id': 'string', 'sc_id': 'string',
                 'vil_id': 'string'}
