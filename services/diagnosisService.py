import json
import time

from flask import jsonify, request, send_file
import base64
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

def delete_file(file_path):
    if os.path.exists(os.path.join(config.UPLOAD_FOLDER, file_path)):
            os.remove(os.path.join(config.UPLOAD_FOLDER, file_path))

def insert_logic():
    try:
        file_result = file_upload()
        if file_result['pred'] == 'retry' or file_result['pred'] == 'foreign_substance':
            delete_file(file_result['description'])
            return jsonify({
                'message': 'success',
                'status': 'OK',
                'description': 'retry',
                'file': "NULL"
                }), 200
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
                'description': pred,
                'file': file_result['description']
            }), 200
        else:
            return jsonify(file_result), 400
    except Exception as e:
        delete_file(file_result['description'])
        return jsonify({
            'message': 'err',
            'status': 'Internal Server err',
            'description': str(e)
        }), 500


def get_logic():
    tasks = table.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify(tasks_list)

def img_logic():
    img_name = request.args.get('img_name', type = str)
    if img_name is None:
        return jsonify({
            'message':"err",
            'status': 'bad request',
            'description': 'check parameter'
            }), 400
    path = os.path.join(config.UPLOAD_FOLDER, img_name)
    if os.path.exists(path):
        f_type = img_name.rsplit('.', 1)[-1].lower()
        if f_type == 'jpeg' or f_type == 'jpg':
            mimetype = 'image/jpeg'
        elif f_type == 'png':
            mimetype = 'image/png'
        return send_file(path, mimetype=mimetype)
    else:
        return jsonify({
            'message': 'err',
            'status': 'bad request',
            'description': 'not exists file'
            }), 400
