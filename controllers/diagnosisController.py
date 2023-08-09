import json
from models.diagnosis import Inserttable, db
from services.diagnosisService import insert_logic, get_logic


def index():
    return{
        'status': 'OK',
        'localhost:3060/diagnosis': '이미지 판단 후 결과 저장 및 반환'
    }


def insert():
    insert_logic()


def get():
    return get_logic()
