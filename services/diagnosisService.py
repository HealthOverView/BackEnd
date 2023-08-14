import json
import time

from flask import jsonify, request
import config
from models.diagnosis import table, db
from werkzeug.utils import secure_filename
import os
from PIL import Image

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.UPLOAD_EXTENSIONS


def file_upload():
    if 'img' not in request.files:
        return {
            'message': 'err',
            'status': 'bad request',
            'description': 'no file part'
        }
    file = request.files['img']
    if file.filename == '':
        return {
            'message': 'err',
            'status': 'bad request',
            'description': 'no selected file'
        }
    image = Image.open(file)
    resize_image = image.resize((640, 640), Image.BICUBIC)
    if resize_image and allowed_file(resize_image.filename):
        try:
            filename = secure_filename(resize_image.filename)
            n_filename = str(time.time_ns()) + "." + filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(config.UPLOAD_FOLDER, n_filename))
            return {
                'message': 'success',
                'status': 'OK',
                'description': n_filename
            }
        except Exception as e:
            return {
                'message': 'err',
                'status': 'Internal Server err',
                'description': str(e)
            }
    else:
        return {
            'message': 'err',
            'status': 'bad request',
            'description': 'Invalid file type'
        }


def insert_logic():
    try:
        file_result = file_upload()
        if file_result['status'] == 'OK':
            #모델 판단 부분
            #이후 결과 result에 저장
            result = 0
            db.session.add(table(diagnosis_date=time.strftime('%Y-%m-%d %H:%M:%S'), img_name=file_result['description'], result=result))
            db.session.commit()
            return jsonify({
                'message': 'success',
                'status': 'OK',
                'description': result
            }), 200
        else:
            return jsonify(file_result), 400
    except Exception as e:
        if os.path.exists(os.path.join(config.UPLOAD_FOLDER, file_result['description'])):
            os.remove(os.path.join(config.UPLOAD_FOLDER, file_result['description']))
        return jsonify({
            'message': 'err',
            'status': 'Internal Server err',
            'description': str(e)
        }), 500


def get_logic():
    tasks = table.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify(tasks_list)
