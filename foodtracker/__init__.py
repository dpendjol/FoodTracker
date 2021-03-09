from flask import Flask
from peewee import SqliteDatabase
from datetime import datetime


db = SqliteDatabase("foodtracker.db")

def create_app(config_filename=None):
    ''' Create the Flask app'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)

    register_blueprints(app)

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    return app

def register_blueprints(app):
    '''
    Register all blueprints in this function
    including the imports
    
    Arguments:
    app -- flask app instance
    '''
    from foodtracker import main
       
    app.register_blueprint(main.main)
