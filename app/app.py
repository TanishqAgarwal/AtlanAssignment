from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    load_dotenv()
    from config.settings import Config
    # Assign configurations from Config class
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')


    # Print loaded environment variables
    print(os.getenv('SQLALCHEMY_DATABASE_URI'))
    print(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))

   

    app.config.from_object(Config)

    db.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    
    return app

