from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Inserttable(db.Model):
    __tablename__ = 'diagnosis'
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diagnosis_date = db.Column(db.Datetime, nullable=False)
    img_name = db.Column(db.String(32), nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<idx %r>' % self.idx


class Gettable(db.Model):
    __tablename__ = 'diagnosis'
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diagnosis_date = db.Column(db.Datetime, nullable=False)
    img_name = db.Column(db.String(32), nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<diagnosis {self.idx}>'
