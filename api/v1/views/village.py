#!/usr/bin/python3
"""Flask routes that return json status response
when endpoints about villages are queried"""
from flask import jsonify, request, abort
# from flasgger import Swagger, swag_from
from api.v1.views import app_views
from etl.models import storage


@app_views.route('/villages', methods=['GET'])
def get_village():
    """Endpoint to return a list of villages"""
    if request.method == 'GET':
        vil_list = storage.all('Village')
        objs_list = []
        for obj in vil_list.values():
            objs_list.append(obj.to_dict())
        return jsonify(objs_list)
