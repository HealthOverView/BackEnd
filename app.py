from flask import Flask
from model.diagnosis import db
from routes.blueprint import blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    return app


app = create_app()
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(host='192.168.1.192', port=3060, debug=True)
