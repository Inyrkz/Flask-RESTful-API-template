'''used to store the setting of the app (database)'''
from flask import Flask

#creating an instance of the flask app
app = Flask(__name__)

#configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
