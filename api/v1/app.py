#!/usr/bin/python3
"""Flask App that serves different data based on the
requested for HTTP endpoint route"""
import os
import yaml
from flask import Flask, make_response, jsonify
from flasgger import Swagger
from etl.models import storage
from api.v1.views import app_views
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s >>> %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)

# Global Flask Application Variable: app
app = Flask(__name__)

swagger_config = 'api/v1/views/swagger.yml'
with open(swagger_config, 'r') as f:
    config = yaml.safe_load(f)

template = {
    'swagger': '2.0',
    'info': {
        'title': config['info']['title'],
        'description': config['info']['description'],
        'version': config['info']['version'],
        'contact': {
            'name': config['info']['contact']['name'],
            'email': config['info']['contact']['email']},
        'termsOfService': config['info']['license']['url']
    },

    'host': config['host'],
    'basePath': config['basePath'],
    'schemes': config['schemes']
}

swagger = Swagger(app, template=template)

# Global Strict Slashes
app.url_map.strict_slashes = False

# app_views Blueprint defined in api.vi.views __init__.py file
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(db):
    """Closes the current SQLAlchemy Session after each HTTP
    request has been executed"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """Handles 404 errors"""
    code = exception.__str__().split()[0]
    description = exception.description
    jsonFile = jsonify({'error': description})
    return make_response(jsonFile, 404)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("DEBUG", True)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=ENVIRONMENT_DEBUG, threaded=True)