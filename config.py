db = {
    'user': 'admin',
    'password': '1q2w3e4r!',
    'host': 'localhost',
    'port': 3306,
    'database': 'Gosari'
}

SQLALCHEMY_DATABASE_URI = f"mysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

UPLOAD_FOLDER = 'images'

UPLOAD_EXTENSIONS = ['jpg', 'png', 'jpeg']
