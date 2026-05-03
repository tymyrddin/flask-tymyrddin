"""
The `bureaucracy` blueprint handles the OT/ICS security bureaucracy simulator.
"""
from flask import Blueprint

bureaucracy_blueprint = Blueprint('bureaucracy', __name__, template_folder='templates')

from . import routes