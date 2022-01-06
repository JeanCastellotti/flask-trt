from flask import Flask
from app.config import Config

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from app.main.routes import main

    app.register_blueprint(main)

    return app