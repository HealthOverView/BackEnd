from flask import Blueprint
from controllers.diagnosisController import index, insert, get, img

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/Test', methods=['GET'])(get)
blueprint.route('/diagnosis', methods=['POST'])(insert)
blueprint.route('/image', methods=['GET'])(img)
