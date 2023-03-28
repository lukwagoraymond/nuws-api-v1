from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/nuws/api/v1.0')
from api.v1.views.waterscheme import *
from api.v1.views.district import *
from api.v1.views.subcounty import *
from api.v1.views.village import *
