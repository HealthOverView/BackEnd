import os
from app001 import app
from werkzeug.utils import secure_filename
from app001.models import Diagnosis

ALLOWED_EXTESIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTESIONS


def upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    else:
        return 'File is missing', 404
    profile_pic_path_and_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(profile_pic_path_and_name)

    # 모델 처리 추가 예정

    return Diagnosis.process(img_name=filename, result=0)
