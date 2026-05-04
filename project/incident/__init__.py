"""
The `incident` blueprint handles the post-incident review generator.
"""
from flask import Blueprint

incident_blueprint = Blueprint('incident', __name__, template_folder='templates')

from . import routes
