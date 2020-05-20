import click
from flask.cli import with_appcontext

from .BookModel import db, Book
from .UserModel import User

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
