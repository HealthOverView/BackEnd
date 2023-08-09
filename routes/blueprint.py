from flask import Blueprint
from controllers.diagnosisController import index, insert, get

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/Test', methods=['GET'])(get)
