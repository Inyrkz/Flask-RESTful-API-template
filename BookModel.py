'''BookModel Database File'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import *

# creating a database object by calling the SQLAlchemy constructor
#  and passing in the app object
db = SQLAlchemy(app)


# the class Book will inherit the db.Model
class Book(db.Model):
    __tablename__ = 'books'  # creating a table name
    # our book has three properties
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False)
    # nullable is false so the column can't be empty
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'name': self.name, 'price': self.price, 'isbn': self.isbn}
        # we want all our output to be in json format so it will be
        # compatible with our flask app
        # this method we are defining will convert our output to json
        # the __repr__ works in the terminal, so we need the json method
        # for the get_all_books() method

    def add_book(_name, _price, _isbn):
        '''function to add book to database using _name, _price,
           _isbn as parameters'''
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        # creating an instance of our Book constructor
        db.session.add(new_book)  # add new book to database session
        db.session.commit()  # commit changes to session

    def get_all_books():
        '''function to get all books in our database'''
        return [Book.json(book) for book in Book.query.all()]

    def delete_book(_isbn):
        '''function to delete a book from our database using
           the isbn of the book'''
        is_successful = Book.query.filter_by(isbn=_isbn).delete()
        # filter by isbn and delete
        db.session.commit()  # commiting the new change to our database
        return bool(is_successful)  # checks if deletion is successful
        # if successful, it will return an integer

    def update_book_price(_isbn, _price):
        '''function to update the price of a book using the isbn of the book
           and the new price of the book as parameters'''
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.price = _price
        db.session.commit()

    def update_book_name(_isbn, _name):
        '''function to update the name of a book using the isbn of the book
            and the new name of the book as parameters'''
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        # replace name with new name in the parameter
        db.session.commit()  # commit changes

    def replace_book(_isbn, _name, _price):
        '''function to replace a book using the book's isbn, new name and
            new price as parameter'''
        book_to_replace = Book.query.filter_by(isbn=_isbn).first()
        book_to_replace.name = _name
        book_to_replace.price = _price
        db.session.commit()  # commit changes

    def get_book(_isbn):
        '''function to retrieve book using the isbn of the book as parameter'''
        return [Book.json(book) for book in Book.query.filter_by(isbn=_isbn).first()]
        # looping through our book list and converting each book object to json
        # in this case, there's only one book
        # the filter_by method filters the query by the isbn
        # the .first() method displays the first value

    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object)
        # the __repr__ is a representation method,
        # it helps us define how we want our data to be represented
