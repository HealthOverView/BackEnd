import json
import time

from flask import jsonify, request
import config
from model.diagnosis import table, db
from werkzeug.utils import secure_filename
import os
from PIL import Image
from API_model import predict

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in config.UPLOAD_EXTENSIONS


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
    #resize_image = image.resize((640, 640), Image.BICUBIC)
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            n_filename = str(time.time_ns()) + "." + filename.rsplit('.', 1)[-1].lower()
            file_path = os.path.join(config.UPLOAD_FOLDER, n_filename)
            image.save(file_path)
            pred = predict(file_path)
            if pred == 'error':
               raise Exception("사진을 다시 찍어주세요")
            return {
                'message': 'success',
                'status': 'OK',
                'description': n_filename,
                'pred': pred
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
            res_list = ['infertility_period', 'transitional_period', 'ovulatory_phase', 'foreign_substance']
            pred = file_result['pred']
            db.session.add(table(diagnosis_date=time.strftime('%Y-%m-%d %H:%M:%S'), img_name=file_result['description'], result=res_list.index(pred)))
            db.session.commit()
            return jsonify({
                'message': 'success',
                'status': 'OK',
                'description': pred
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
