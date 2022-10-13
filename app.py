from datetime import date, datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config ['JSON_SORT_KEYS'] = False

# Universal way to specify a database connection: URI
# Sets up everything we need to run the flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:5432/trello'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Card(db.Model):
    __tablename__ = 'cards'
    # Define number of columns: Name, constraints, datatype, primary/foreign key
    # Searches and finds attributes
    # DECLARE FIELDS (COLUMNS)
    id =            db.Column(db.Integer, primary_key=True)
    title =         db.Column(db.String(100))
    description =   db.Column(db.Text)
    date =          db.Column(db.Date)
    status =        db.Column(db.String)
    priority =      db.Column(db.String)
    # `primary_key=True` will automatically be of a Serial datatype

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'priority', 'date')
        ordered = True

# Define a custom CLI (terminal) command
@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

# Seeding the database: Sample data 
@app.cli.command('seed')
def seed_db():
    card = Card(
        title = 'Start the project',
        description = 'Stage 1 - Creating the Database',
        status = 'To Do',
        priority = 'High',
        date = date()
    )

@app.cli.command('seed')
def seed_db():
    cards = [
        # List of instances of Card
        # Add all 
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today()
        ),
        Card(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today()
        ),
        Card(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        ),
        Card(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        )
    ]

    db.session.add_all(cards)
    db.session.commit()
    print('Tables seeded')

@app.route('/cards/')
def all_cards():
    # SQL EQUIVALENT GOAL
    # select * from cards;
    
    # LEGACY METHOD
    # cards = Card.query.all()
    # print(cards)
    # print(cards[0].__dict__)
    
    # NEW METHOD
    # stmt = db.select(Card).where(Card.status == 'Ongoing', Card.priority == 'High')
    # stmt = db.select(Card).filter_by(status = 'To Do')
    # stmt = db.select(Card).where(db.or_(Card.status == 'To do',  Card.priority == 'High'))
    # stmt = db.select(Card).where(Card.id > 2)

    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)
    cards = db.session.scalars(stmt)
    # Converts to standard python datatypes:
    return CardSchema(many=True).dump(cards)
    # print(stmt)
    # print(stmt)
    # print(cards)
    # print(cards[0].__dict__)

@app.cli.command('first_card')
def first_card():
    # select * from cards limit 1;
    # Parameterized query (limit 1)
   
    # LEGACY METHOD
    # cards = Card.query.first()
    # print(cards.__dict__)

    # NEW METHOD
    stmt = db.select(Card).limit(1)
    card = db.session.scalar(stmt)
    print(stmt)
    print(card.__dict__)

@app.cli.command('count_ongoing')
def count_ongoing():
    stmt = db.select(db.func.count()).select_from(Card).filter_by(status='Ongoing')
    cards = db.session.scalar(stmt)
    print(cards)

# Homepage
@app.route('/')
def index():
    return "Hello, world!"

