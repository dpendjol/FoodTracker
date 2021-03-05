from flask import Flask
from main.routes import main
from extensions import db


app = Flask(__name__)
app.secret_key = "justakey"

app.register_blueprint(main)    
  
@app.before_request
def before_request():
    """Connect to the database before each request"""
    db.connect()


@app.after_request
def after_request(response):
    """Close the database after each request"""
    db.close()
    return response

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    pass