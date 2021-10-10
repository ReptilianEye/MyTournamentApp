from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"  # nazwa bazy danych

def create_app():
    app = Flask(__name__)
    # secret key to things like cookie etc
    app.config['SECRET_KEY'] = 'kjabwdlajbal'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # inicjowanie bazy danych dla aplikacji


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_datebase(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_datebase(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Datebase!')
