from flask import Flask

app = Flask(__name__)

from lab.views import user
from lab.views import category
from lab.views import record