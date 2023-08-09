import json
import time

from flask import jsonify, request
import config
from models.diagnosis import table, db
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.UPLOAD_EXTENSIONS


def file_upload():
    if 'img' not in request.files:
        return jsonify({
            'message': 'err',
            'status': 'bad request',
            'description': 'no file part'
        })
    file = request.files['img']
    if file.filename == '':
        return jsonify({
            'message': 'err',
            'status': 'bad request',
            'description': 'no selected file'
        })
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            n_filename = time.time_ns()+"."+filename
            file.save(os.path.join(config.UPLOAD_FOLDER, n_filename))
            return jsonify({
                'message': 'success',
                'status': 'OK',
                'description': n_filename
            })
        except Exception as e:
            return jsonify({
                'message': 'error',
                'status': 'Internal Server err',
                'description': str(e)
            })
    else:
        return jsonify({
            'message': 'error',
            'status': 'bad request',
            'description': 'Invalid file type'
        })


def insert_logic():
    file_result = file_upload()
    if file_result['status']=='OK':
        pass
    else:
        return file_result


def get_logic():
    tasks = table.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify(tasks_list)
