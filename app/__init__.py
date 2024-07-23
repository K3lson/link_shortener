from flask import Flask
from .models import db

#create the app

def create_app():
    #configure the SQLite database, relative to the app instance folder
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'  # This is the correct format
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #initialize the app with the extention
    db.init_app(app)

    with app.app_context():
        db.create_all()


    from .routes import main
    app.register_blueprint(main)


    return app