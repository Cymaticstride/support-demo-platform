import os

from dotenv import load_dotenv
from flask import Flask

from .extensions import db


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-key"

    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = os.getenv("DB_PORT", "3307")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "123456")
    db_name = os.getenv("DB_NAME", "support_demo")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from . import models
    from .routes import main_bp

    app.register_blueprint(main_bp)

    return app