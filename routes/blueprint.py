from flask import Blueprint
from controllers.diagnosisController import index, insert, get

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', method=['GET'])(index)
blueprint.route('/Test', method=['GET'])(get)
