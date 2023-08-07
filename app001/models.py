from flask_mysqldb import Mysql
from app001.routes import app

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '1q2w3e4r!'
app.config['MYSQL_DB'] = 'Gosari'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
