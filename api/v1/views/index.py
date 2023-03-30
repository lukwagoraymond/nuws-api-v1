#!/usr/bin/python3
"""Index HTTP Endpoint Route"""
from flask import jsonify, request, make_response
# from flasgger import Swagger, swag_from
from api.v1.views import app_views
from api.v1.views import logger
import subprocess
import os


@app_views.route('/fetch', methods=['GET'])
def fetch_kobo_data():
    """Endpoint runs the main.py file as if in the
    shell console"""
    if request.method == 'GET':
        python_cmd = ['python3', '-m', 'etl.main', 'https://kc.kobotoolbox.org/api/v1/data/1330078']
        file_path = subprocess.check_output(python_cmd, universal_newlines=True)
        logger.info(file_path)
        payload = jsonify({'message': 'SUCCESS: Fetched all Data from Kobo Toolbox'})
        if file_path is not None:
            return make_response(payload, 200)
