from flask import Flask
from app.config import config
from app.extensions import db
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    
    from app import models

    with app.app_context():
        db.create_all()

    from app.api import api_bp
    app.register_blueprint(api_bp)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
