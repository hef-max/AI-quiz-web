from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Inisialisasi database dan login manager
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)

    # Konfigurasi aplikasi
    app.config['SECRET_KEY'] = '123mans081/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Menginisialisasi database dan login manager
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)


    # Blueprint
    from app.auth_routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from app.routes import main
    app.register_blueprint(main)

    return app
