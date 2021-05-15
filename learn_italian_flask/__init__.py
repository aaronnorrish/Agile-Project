from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from learn_italian_flask import routes, models, errors, controllers

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/learn_italian.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Learn Italian startup')


# admin = Admin(app)
admin = Admin(app, "Learn Italian — Admin", index_view=controllers.CustomAdminIndexView())
admin.add_view(controllers.CustomModelView(routes.User, db.session))
admin.add_view(controllers.CustomModelView(routes.Quiz, db.session))
admin.add_view(controllers.CustomModelView(routes.UserAnswer, db.session))

if __name__ == "__main__":
    app.run()
