##서비스 파일-핵심 실행 내용
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

##받은 파일 확장자 확인 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in config.UPLOAD_EXTENSIONS

##파일 저장하는 함수
def file_upload():
    #img 파라미터 확인
    if 'img' not in request.files:
        return {
            'message': 'err',
            'status': 'bad request',
            'description': 'no file part'
        }
    file = request.files['img']
    #이미지 파일이 없을 떄
    if file.filename == '':
        return {
            'message': 'err',
            'status': 'bad request',
            'description': 'no selected file'
        }
    image = Image.open(file)
    #확장자 확인후 저장 
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
    #지원하지 않는 파일 등록시
    else:
        return {
            'message': 'err',
            'status': 'bad request',
            'description': 'Invalid file type'
        }

#파일 지우는 함수
def delete_file(file_path):
    if os.path.exists(os.path.join(config.UPLOAD_FOLDER, file_path)):
            os.remove(os.path.join(config.UPLOAD_FOLDER, file_path))

##결과를 데이터베이스에 저장하고 반환하는 함수
def insert_logic():
    try:
        file_result = file_upload()
        #결과가 이물질, 재시도일때
        if file_result['pred'] == 'retry' or file_result['pred'] == 'foreign_substance':
            delete_file(file_result['description'])
            return jsonify({
                'message': 'success',
                'status': 'OK',
                'description': 'retry',
                'file': "NULL"
                }), 200
        #결과가 이물질과 재시도가 아닐떄
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
        #결과에 문제가 있을떄
        else:
            return jsonify(file_result), 400
    except Exception as e:
        delete_file(file_result['description'])
        return jsonify({
            'message': 'err',
            'status': 'Internal Server err',
            'description': str(e)
        }), 500


##테이블 내 모든 데이터 반환 함수
def get_logic():
    tasks = table.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify(tasks_list)

##이름에 해당하는 이미지를 반환하는 함수
def img_logic():
    img_name = request.args.get('img_name', type = str)
    #이미지 이름이 없을 떄 
    if img_name is None:
        return jsonify({
            'message':"err",
            'status': 'bad request',
            'description': 'check parameter'
            }), 400
    path = os.path.join(config.UPLOAD_FOLDER, img_name)
    #해당 이름의 파일이 존재할 떄
    if os.path.exists(path):
        f_type = img_name.rsplit('.', 1)[-1].lower()
        if f_type == 'jpeg' or f_type == 'jpg':
            mimetype = 'image/jpeg'
        elif f_type == 'png':
            mimetype = 'image/png'
        return send_file(path, mimetype=mimetype)
    #해당 이름의 파일이 없을 떄
    else:
        return jsonify({
            'message': 'err',
            'status': 'bad request',
            'description': 'not exists file'
            }), 400
