#!/usr/bin/python3
"""Flask routes that return json status response
when endpoints about districts are queried"""
from flask import jsonify, request, abort
from flasgger import Swagger, swag_from
from api.v1.views import app_views
from etl.models import storage
import json


@app_views.route('/districts', methods=['GET'])
def get_districts():
    """Endpoint to return a list of water supply systems"""
    if request.method == 'GET':
        wss_list = storage.all('District')
        objs_list = []
        for obj in wss_list.values():
            objs_list.append(obj.to_dict())
        return jsonify(objs_list)
