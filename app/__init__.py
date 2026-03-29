from flask import Flask, redirect
from flask_smorest import Api

from .config import Config
from .models import db
from .presentation.api import blp as import_blp
from .presentation.web import web_bp


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    db.init_app(app)
    api = Api(app)
    api.register_blueprint(import_blp)
    app.register_blueprint(web_bp)

    @app.get("/")
    def index():
        return redirect("/policies")

    return app
