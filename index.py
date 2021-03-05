from flask import Flask
from main.routes import main


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

if __name__ == '__main__':
    pass