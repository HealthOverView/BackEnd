import json

from flask import jsonify

from models.diagnosis import Inserttable, db
#import request
from werkzeug.utils import secure_filename
import os


def insert_logic():
    pass
    # file = request.files['img']
    #
    # filename = secure_filename(file.filename)
    # os.makedirs(image_path, exists_ok=True)
    # file.save()


def get_logic():
    tasks = Inserttable.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify(tasks_list)
