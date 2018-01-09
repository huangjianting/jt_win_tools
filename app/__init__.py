# coding:utf-8
from flask import Flask
from flask_login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import local_db


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = local_db
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.api import api as win_service_blueprint
    app.register_blueprint(win_service_blueprint, url_prefix='/api')
    db.init_app(app)
    login_manager.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    db.create_all(app=app)
