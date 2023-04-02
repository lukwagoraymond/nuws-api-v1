#!/usr/bin/python3
"""Flask routes that return json status response
when endpoints about water supply schemes are queried"""
from flask import jsonify, request, abort
from flasgger import swag_from
from api.v1.views import app_views
from etl.models import storage


@app_views.route('/schemes', methods=['GET'])
@swag_from('doc/schemes.yml', methods=['GET'])
def water_schemes():
    """Endpoint to return a list of water supply systems"""
    if request.method == 'GET':
        wss_list = storage.all('WaterScheme')
        objs_list = []
        for obj in wss_list.values():
            objs_list.append(obj.to_dict())
        return jsonify(objs_list)
