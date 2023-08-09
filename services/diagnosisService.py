import json
from models.diagnosis import Inserttable, db, Gettable
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
    return Gettable.query.all()