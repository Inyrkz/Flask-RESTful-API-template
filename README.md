# Flask-RESTful-API-template
This template shows how to build a RESTful API with Flask

I created a simple book model for a book store.
I used various http methods such as GET, POST, PUT, PATCH and DELETE to create API routes.

A database was created using SQLAlchemy to store data about books.
The GET request is used to get all the books in the .
The POST is used to add new books to the database.
The PUT is used to replace or update a book.
The PATCH is used to edit an entity of the book.
The DELETE is used to remove a book from the database.

JWT (Json Web Token) was used to give users token after they have been authenticated

To run this file:
- Install all the dependencies in the requirements.txt file by running:
  pip install -r requirements.txt
- Run the app.py file
