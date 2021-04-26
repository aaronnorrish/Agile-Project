from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from learn_italian_flask import routes