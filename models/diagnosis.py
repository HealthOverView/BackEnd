from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class table(db.Model):
    __tablename__ = 'diagnosis'
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diagnosis_date = db.Column(db.DateTime, nullable=False)
    img_name = db.Column(db.String(32), nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<idx %r>' % self.idx

    def formatted_diagnosis_date(self, format='%Y-%m-%d %H:%M:%S'):
        return self.diagnosis_date.strftime(format)

    def to_dict(self):
        return {
            'idx': self.idx,
            'diagnosis_date': self.diagnosis_date,
            'img_name': self.img_name,
            'result': self.result
        }
