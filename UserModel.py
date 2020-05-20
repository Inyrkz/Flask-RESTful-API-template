from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) #username must be unique
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):  
        '''this representation method makes our output easy to read,
            specifically it returns a printable representation of an object, it helps us troubleshoot and 
            make sure things are working the way they should'''
        return str({
            "username": self.username,
            "password": self.password
        })
        
    def username_password_match(_username, _password):
        '''this method checks if the password and username sent to us, match that in the database'''
        user = User.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True

    def getAllUsers():
        '''function to return all users'''
        return User.query.all()

    def createUser(_username, _password):
        '''function to create new user using username and password as parameters'''
        new_user = User(username = _username, password = _password)
        db.session.add(new_user)
        db.session.commit()
        