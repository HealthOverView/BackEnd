from flask_mysqldb import Mysql
from app001.routes import app

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '1q2w3e4r!'
app.config['MYSQL_DB'] = 'Gosari'
app.config['MYSQL_PORT'] = 3306
app.config['UPLOAD_FOLDER'] = './imageData'

mysql = MySQL(app)


class Diagnosis:
    def process(self, img_name, result):
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO diagnosis(diagnosis_date, img_name, result) VALUES (now(), %s, %d)''', img_name,
                    result)
        rv = cur.fetchall()
        return str(rv)
