
## 제한사항
리눅스(우분투)에서 실행하는 것을 전제로 개발/작성되었습니다

wget 패키지가 사전에 설치 되어있어야 합니다

## 사전준비
### Maria-db로 테이블 구성
~~~
CREATE TABLE diagnosis(
  idx int primary key auto_increment,
  diagnosis_date datetime not null,
  img_name varchar(32) not null
  result int not null,
);
~~~

### config.py 작성
~~~
#db관련 설정
db = {
    'user': '사용자명',
    'password': '비밀번호',
    'host': 'localhost',
    'port': 3306,
    'database': '데이터베이스명'
}

SQLALCHEMY_DATABASE_URI = f"mysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

#이미지 저장 경로
UPLOAD_FOLDER = 'images'

#이미지 확장자 설정
UPLOAD_EXTENSIONS = ['jpg', 'png', 'jpeg']

#서버IP
SERVER_NAME = '서버IP:PORT'

#디버그모드 설정
DEBUG = False
~~~
해당 내용 작성 후 실행하기 전 폴더에 저장

## 실행 단계
1. cmd에서 해당 폴더로 이동
2. sh init.sh 명령어 실행
3. python app.py 명령어 실행
