import os

from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flaskr import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)
    app.secret_key = 'dev'

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app