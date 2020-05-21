from flask import Flask, request, Response, jsonify
from BookModel import *
from UserModel import User
from settings import *

import json
import jwt, datetime
from functools import wraps
#jwt(JSON Web Token) handles authentication of API without client sending us username and password for every API call

app.config['SECRET_KEY'] = 'meow' #defining secret key

@app.route('/login', methods=['POST'])
def get_token():
    '''function to get token to access API using the /login URI'''
    request_data = request.get_json()
    username = str(request_data['username'])
    password =  str(request_data['password']) #it needs to be a string, since we will be comparing the value

    match = User.username_password_match(username, password) #use the username_password_match method

    if match:    
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        #setting the expiration date of our token. datetime.datetime.utcnow() is the exact time the user will access the route.
        #datetime.timedelta(seconds=100) time is set to 100 seconds
        #so therefore, the expiration date is 100 seconds after token is received
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        # first parameter is a dictionary containing the expiration date
        #second parameter contains the secret key defined earlier
        #third is the algorithm to be used which is HS256 in this case
        return token
    else:
        return Response('', 401, mimetype='application/json')


#defining our decorator
#creating a decorator for token authentication
#decorator can be called by using @token_required
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            #decodes the token passed in the URI
            return f(*args, **kwargs)
        except:
            return jsonify({'error' : 'Need a valid token to view this page'}), 401
            #if token is invalid, it returns an error message with 401 status code
    return wrapper


#GET /books?token=arfdanlkjkr879489798797
@app.route('/books')#GET method is default
def get_books():
    '''Function to get our list of books'''
    return jsonify({'books' : Book.get_all_books()}) #if token is valid, then the books are displayed
    

#sanitizing data sent in post request
#we don't want clients to send just any data to our API, we need to validate the data sent to the server
def validBookObject(bookObject):
    '''Function that validates the data sent to our API'''
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

def validBookObjectPut(bookObject):
    '''Function that validates the data sent to our API'''
    if ("name" in bookObject and "price" in bookObject):
        return True
    else:
        return False
        
def validBookObjectPatch(bookObject):
    '''Function that validates the data sent to our API'''
    if ("name" in bookObject or "price" in bookObject):
        return True
    else:
        return False


# adding new books using Post
@app.route('/books', methods=['POST'])#using POST method to send data to our API using the same url '/books'
@token_required
def add_book():
    '''Function to add new books to our list of books'''
    request_data = request.get_json() #getting data from client
    if (validBookObject(request_data)): #if True
        Book.add_book(request_data["name"], request_data["price"], request_data["isbn"])
        response = Response("", 201, mimetype='application/json') # 3 parameters, the first is the response body, second is the status code and third is the content type header that will be sent back to the client
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        # The response body is an empty string because the client won't get access to the resource from the response body but from the location header instead.
        #  A location header points to where a client can go and receive the new resource that was created
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this 'name': 'booktitle', 'price': 760, 'isbn': 394547832933408"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
# we return an error and help message to user when they send a bad request
# 400 is status code for bad request
# json.dumps converts dictionary to json, import json first  
# Note: when we return a string in flask, it automatically sets the response type to text.html and the status code to 200 (successful)


#getting info about the book directly by using the isbn in the url
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value) 

#PUT; updating a book in our list
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if (not validBookObjectPut(request_data)): #if True
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this 'name': 'booktitle', 'price': 760, 'isbn': 394547832933408"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
        # The response body is an empty string because the client won't get access to the resource from the response body but from the location header instead.
        #  A location header points to where a client can go and receive the new resource that was created
              
    Book.replace_book(isbn, request_data['name'], request_data['price'])    
    response = Response("", status=204) #204 means no content response
    return response

#PATCH; updating an entry of a book in our list
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if (not validBookObjectPatch(request_data)): #if True
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this 'name': 'booktitle', 'price': 760, 'isbn': 394547832933408"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
        # The response body is an empty string because the client won't get access to the resource from the response body but from the location header instead.
        #  A location header points to where a client can go and receive the new resource that was created

    if ("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
    if ("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
        
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    '''Function to delete book based on isbn'''
    if (Book.delete_book(isbn)):
        response = Response("", status=204)
        return response

    invalidBookObjectErrorMsg = {
        "error":"Book with the ISBN number that was provided was not found, so therefore unable to delete book"
    }    
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response


#if __name__ == "__main__":
    #app.run(debug=True)
app.run(port=5000)
