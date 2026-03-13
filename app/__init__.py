from flask import Flask

from .config import Config
from .models import db


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    db.init_app(app)
    return app
