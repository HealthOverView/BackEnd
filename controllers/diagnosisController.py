import json
from models.diagnosis import table, db
from services.diagnosisService import insert_logic, get_logic


def index():
    return{
        'status': 'OK',
        'localhost:3060/diagnosis': '이미지 판단 후 결과 저장 및 반환'
    }


def insert():
    insert_logic()
    return "test 중입니다..."


def get():
    return get_logic()
