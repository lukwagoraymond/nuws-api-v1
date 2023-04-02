#!/usr/bin/python3
"""Flask routes that return json status response
when endpoints about sub-counties are queried"""
from flask import jsonify, request, abort
from flasgger import swag_from
from api.v1.views import app_views
from etl.models import storage


@app_views.route('/sub_counties', methods=['GET'])
@swag_from('doc/subcounties.yml', methods=['GET'])
def get_sc():
    """Endpoint to return a list of Sub-Counties"""
    if request.method == 'GET':
        sc_list = storage.all('SubCounty')
        objs_list = []
        for obj in sc_list.values():
            objs_list.append(obj.to_dict())
        return jsonify(objs_list)
