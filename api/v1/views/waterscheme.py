#!/usr/bin/python3
"""Flask routes that return json status response
when endpoints about water supply schemes are queried"""
from flask import jsonify, request, abort
from flasgger import Swagger, swag_from
from api.v1.views import app_views
from etl.models import storage
from etl.models.waterscheme import WaterScheme


@app_views.route('/waterschemes', methods=['GET'])
def water_schemes():
    """Endpoint to return a list of water supply systems"""
    if request.method == 'GET':
        wss_list = storage.all('WaterScheme')
        objs = [obj.to_dict() for obj in wss_list.values()]
        return jsonify(objs)


@app_views.route('/waterschemes/<scheme_id>', methods=['GET'])
def water_schemes_id(scheme_id=None):
    """Endpoint to return the details of a water supply system based
    on name entered - to be changed later"""
    scheme_obj = storage.get_obj('WaterScheme', scheme_id)
    if not scheme_obj:
        abort(404, 'Water Supply Scheme Name requested is not Found')
    if request.method == 'GET':
        return jsonify(scheme_obj.to_dict())
