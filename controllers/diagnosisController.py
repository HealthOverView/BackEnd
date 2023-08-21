import json
from model.diagnosis import table, db
from services.diagnosisService import insert_logic, get_logic, img_logic


def index():
    return{
        'status': 'OK',
        'localhost:3060/diagnosis': '이미지 판단 후 결과 저장 및 반환'
    }

def insert():
    return insert_logic()


def get():
    return get_logic()

def img():
    
    return img_logic()
