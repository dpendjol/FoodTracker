from flask import Flask
from peewee import SqliteDatabase
from datetime import datetime
import os


db = SqliteDatabase("foodtracker.db")

def create_app(test_config=None):
    ''' Create the Flask app'''
    # second argument
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'foodtracker.db'),
    )
    print(app.instance_path)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    register_blueprints(app)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
