##라우트에 따라 각 서비스 호출
import json
from model.diagnosis import table, db
from services.diagnosisService import insert_logic, get_logic, img_logic


def index():
    return{
        'status': 'OK',
        '/diagnosis': '이미지 판단 후 결과 저장 및 반환',
        '/Test': '데이터 베이스 내 데이터 출력',
        '/image':'파일명을 받아 해당 파일 반환' 
    }

def insert():
    return insert_logic()


def get():
    return get_logic()

def img():
    
    return img_logic()
