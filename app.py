from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Universal way to specify a database connection: URI
# Sets up everything we need to run the flask application
app.config['SQLACHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:8080/trello'

db = SQLAlchemy(app)

print(db.__dict__)

@app.route('/')
def index():
    return "Hello, world!"