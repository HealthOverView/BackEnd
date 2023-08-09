db = {
    'user': 'admin',
    'password': '1q2w3e4r!',
    'host': 'localhost',
    'port': 3306,
    'database': 'diagnosis'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

UPLOAD_FOLDER = './images'