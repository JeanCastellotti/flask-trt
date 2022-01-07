import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Environment, Bundle
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_assets(app):
    assets = Environment(app)
    assets.load_path = [os.path.join(os.path.dirname(__file__), 'src')]
    stylus = Bundle('css/main.styl', depends=('css/partials/*.styl'), filters='stylus,autoprefixer6,cssmin', output='css/style.css')
    assets.register('stylus', stylus)


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    create_assets(app)

    from app.main.routes import main

    app.register_blueprint(main)

    return app