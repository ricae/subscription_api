from flask_restx import Api
from models import db
import endpoints
import os

def setup_database(app):
  
    # Initialize the database
    env = os.getenv('FLASK_ENV', 'testing')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    elif env == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

def setup_application(app):
    api = Api(app, doc="/swagger-ui")
    endpoints.register(api)

