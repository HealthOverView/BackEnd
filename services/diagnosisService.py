import json

from flask import jsonify, request
from app import app
from models.diagnosis import table, db
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({
                'message': 'success',
                'status': 'OK',
                'description': 'file upload success'
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
    return file_upload()
    # os.makedirs(image_path, exists_ok=True)
    # file.save()


def get_logic():
    tasks = table.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify(tasks_list)
