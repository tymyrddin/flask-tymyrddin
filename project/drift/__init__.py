"""
The `drift` blueprint serves the truth drift engine: a four-stage reveal
of how a stated control behaves once operational reality and incentives
get involved.
"""
from flask import Blueprint

drift_blueprint = Blueprint('drift', __name__, template_folder='templates')

from . import routes
