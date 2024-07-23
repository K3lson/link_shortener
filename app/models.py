from flask_sqlalchemy import SQLAlchemy
import string
import random

#initialize SQLAlchemy object

db = SQLAlchemy()

#Define URL model

class URL(db.Model):
    #Define columns in the URL table
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(6), unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())


    #Initialize URL instance
    def __init__(self, original_url):
        self.original_url = original_url
        self.short_url = self.generate_short_link()


    #Generate a unique short link
    def generate_short_link(self):
        #Define character to use in short URL
        characters = string.ascii_letters + string.digits
        short_url = " ".join(random.choices(characters, k=6))

        #Check if the short URL already exists
        link = self.query.filter_by(short_url = short_url).first()

        #If it exists, generate a new short URL until it is unique
        while link:
            short_url = " ".join(random.choices(characters, k=6))
            link = self.query.filter_by(short_url=short_url).first()
        
        return short_url