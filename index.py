from flask import Flask
from main.routes import main


def create_app():
    app = Flask(__name__)
    app.secret_key = "justakey"
    
    app.register_blueprint(main)    
    
    return app

if __name__ == '__main__':
    create_app()