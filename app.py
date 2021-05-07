from flask import Flask

from handlers.db import init_db
from handlers.routes import configure_routes

SHORT_DATA_PATH = 'sample-data/patients-short.json'
DATA_PATH = 'sample-data/patients.json'


def create_app(path=DATA_PATH):
    app = Flask(__name__)
    app.db = init_db(path=path)
    configure_routes(app)
    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0')
