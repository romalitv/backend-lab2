from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

from lab.views import user
from lab.views import category
from lab.views import record