import json

from flask import jsonify, request

from models.diagnosis import table, db
from werkzeug.utils import secure_filename
import os


def insert_logic():
    file = request.files['img']
    filename = secure_filename(file.filename)
    print(filename)
    # os.makedirs(image_path, exists_ok=True)
    # file.save()


def get_logic():
    tasks = table.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify(tasks_list)
