import os
from flask import Flask
from flask_cors import CORS
from .api import blueprint as api_blueprint
from .db import redis_store


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if app.config["ENV"] == "production":
        app.config.from_object("default_config.ProductionConfig")
    else:
        app.config.from_object("default_config.DevelopmentConfig")

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile("config.py", silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)
    redis_store.init_app(app)
    app.register_blueprint(api_blueprint, url_prefix="/v1")

    return app
