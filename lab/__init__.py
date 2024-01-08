from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from lab.models import UserModel, RecordModel, CategoryModel


import lab.views.user
import lab.views.record
import lab.views.category