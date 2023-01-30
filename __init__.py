from configparser import ConfigParser

import json
from flask import Flask, render_template, request
import config


def create_app():
    app = Flask(__name__)
    #if app.config["ENV"] =="production":
    #    app.config.from_object(config.ProductionConfig)
    #elif app.config["ENV"] =="testing":
    #    app.config.from_object(config.TestingConfig)
    #else:
    app.config.from_object(config.DevelopmentConfig)
    print(app.config)

    from application.views import views

    app.register_blueprint(views, url_prefix='/')

    #import application.models as models
    return app

