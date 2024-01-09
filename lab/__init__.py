from flask import Flask
from flask_migrate import Migrate

from .db import db
from lab.models import UserModel, RecordModel, CategoryModel

import lab.views.record
import lab.views.category


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(lab.views.category)
    app.register_blueprint(lab.views.record)
    app.register_blueprint(lab.views.user)

    return app