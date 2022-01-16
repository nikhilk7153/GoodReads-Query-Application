from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)
from sources.scraper.Book import Book
from sources.scraper.Author import Author
from sources.api.QueryParser import QueryParser

mongo = client = MongoClient("mongodb+srv://nikhilk5:fluffy63@cluster0.pj5mb.mongodb.net/Goodreads?retryWrites=true&w=majority")
db = mongo["Goodreads"]
serverStatusResult = db.command("serverStatus")

CORS(app)

'''
The app.py class is meant to serve as a code base for the handling the backend logic for API calls. Specifically, this 
class maintains the logic for when a user wants to insert new books and authors, delete books and authors with a specific id, 
inserting new information about a book or id from the user's input with a provided json, and getting books based off the 
query parsing syntax or though the id. 
'''
def docFromID(object, field, id_value):
    '''
    Returns the document from the id, if possible
    :param object: the collection which will be traversed through
    :param field: either book_id/author_id which will specify to the mongodb query which field to search for
    :param id_value: the id-value of the author or book
    :return: The result of the query along with an HTTP response that will get sent back to the function that called it
    '''
    print("Line 31")
    print(id_value.isdigit())
    if id_value == "" or (id_value.isdigit()) is False:
        return {"Result": dumps([]), "HTTP Response":  400}

    document = list(db.get_collection(object).find({field: int(id_value)}))

    if len(document) == 0:
        return {"Result": dumps([]), "HTTP Response": 404}
    else:
        return {"Result": dumps(document), "HTTP Response": 200}


def insertItems(object, json):
    '''
    Function inserts all of the items into the object database
    :param object: the database that will be used
    :param json: the file that will get added to the database
    '''

    json = eval(json)
    array = json["collection"]

    for i in range(len(array)):
        db.get_collection(object).insert(array[i])


@app.route('/book', methods=["GET"])
def getBook():
    '''
    Function returns the book information as a json if the id of the book exists and returns an HTTP response as well
    :return: the result of the outcome from parsing (either a json or an error message) and an HTTP response
    '''

    id_value = request.args.get('id', '')
    result = docFromID("book", "book_id", id_value)
    return result["Result"], result["HTTP Response"]

@app.route('/book/list_all', methods=["GET"])
def getAllBooks():
    '''
        Function returns the book information as a json for all authors
        :return: the result of the outcome from parsing (either a json or an error message) and an HTTP response
    '''
    try:
        books = db.get_collection("book").find()
        return dumps(list(books)), 200
    except:
        return "No books found", 404

@app.route('/author/list_all', methods=["GET"])
def getAllAuthors():
    '''
        Function returns the author information as a json for all authors
        :return: the result of the outcome from parsing (either a json or an error message) and an HTTP response
    '''

    authors = db.get_collection("author").find()
    return dumps(list(authors)), 200



@app.route('/author', methods=["GET"])
def getAuthor():
    '''
        Function returns the book information as a json if the id of the author exists and returns an HTTP response
        :return: the result of the outcome from parsing (either a json or an error message) and an HTTP response
    '''

    id_value = request.args.get('id', '')
    result = docFromID("author", "author_id", id_value)
    return result["Result"], result["HTTP Response"]


@app.route('/search', methods = ["GET"])
def getQuery():
    '''
        Function returns the result of the query search if successful, or an error message if the method was successful
        :return: the result of the outcome from parsing (either a json or an error message) and an HTTP response
    '''

    query = request.args.get('q', '')
    try:
        query = QueryParser.createSeparateQueries(query)
        return query, 200
    except:
        return "The query you have entered has an improper syntax", 400

@app.route('/book', methods=["PUT"])
def putBook():
    '''
    Updates the infomration for the book in question based on it's id through the json file that is given
    :return the status message along with an HTTP response
    '''
    print("line 113")
    id_value = request.args.get('id', '')
    print(id_value)
    print(type(request.get_json()))
    return putHelper("book", "book_id", id_value, request.get_json())

@app.route('/author', methods=["PUT"])
def putAuthor():
    '''
       Updates the information for the author in question based on it's id through the json file that is given
       :return the status message along with an HTTP response
    '''
    id_value = request.args.get('id', '')
    return putHelper("author", "author_id", id_value, request.get_json())


def putHelper(object, field, id_value, json):
    '''
    Helper function which will help take in information about the object and update the database accordingly
    :param object: the object which specifies which database to update
    :param field: the field which will tell MongoDB to search for either a book_id or a author_id
    :param id_value: the id value of the author or book
    :param json: the json values that needs to get updated
    :return: the message and the HTTP response
    '''

    result = docFromID(object, field, id_value)

    if json is None:
        return "The input data is not JSON formatted", 415
    else:
        if result["HTTP Response"] == 200:
            db.get_collection(object).find_one_and_update({field: int(id_value)}, {"$set": json})
            return {"Result": "Insertion of " + object + " successful with id " + id_value, "HTTP Response": 200}
        else:
            return result["Result"], result["HTTP Response"]

def formatJson(json):
    '''
    :param json: json string
    :return: the json object without any backslaches or double quotes
    '''
    if isinstance(json, str) and json.startswith('"') and json.endswith('"'):
        json = json[1:-1]
        json = json.replace("\\", '')

    return json

@app.route('/book', methods = ["POST"])
def addBook():
    '''
    Function adds a book to the book database based on the book call
    :return: A message and an HTTP response
    '''
    print("Line 167")
    print(request.get_json())
    json = request.get_json()
    if json is not None:
        if "collection" in json:
            return "Function can only add one book", 400
        else:
            db.get_collection("book").insert(json)
            return "Successful", 200
    else:
        return "The input data is not JSON formatted", 415

@app.route('/books', methods=["POST"])
def addBooks():
    '''
        Function adds multiple books to the book database based the json items that get passed in
        :return: A message and an HTTP response
    '''

    if request.get_json() is not None:
        insertItems("book", request.get_json())
        return "Successful", 200
    else:
        return "The input data is not JSON formatted", 415


@app.route('/author', methods = ["POST"])
def addAuthor():
    '''
        Function adds an author to the author database based the json items that get passed in
        :return: A message and an HTTP response
    '''
    json = request.get_json()

    if json is not None:
        db.get_collection("author").insert(json)
        return "Successful", 200
    else:
        return "The input data is not JSON formatted", 415

@app.route('/authors', methods = ["POST"])
def addAuthors():
    '''
        Function multiple authors to the book database based on the book call
        :return: A message and an HTTP response
    '''
    if request.get_json() is not None:
        insertItems("author", request.get_json())
        return "Authors have been successfully added", 200
    else:
        return "The input data is not JSON formatted", 415

@app.route('/scrape', methods=["POST"])
def scrape():
    '''
    Scrapes a certain number of books and authors that gets specified by the user
    :return: A message about the result and an HTTP Response
    '''

    object = request.args.get('object', '')
    total = request.args.get('total', '')
    startingLink = request.args.get('link', '')

    try:
        if object == 'author':
            author_database = Author(startingLink, int(total), None)
            author_database.scrapeAuthors()
            return "Successful", 200
        elif object == 'book':
            book_database = Book(startingLink, int(total), None)
            book_database.scrapeBooks()
            return "Successful", 200
        else:

            return "The database name is not valid", 400
    except:
        return "A entry that was entered is not valid", 400

@app.route('/book', methods=["DELETE"])
def deleteBook():
    '''
    Deletes a book based on the id given
    :return: A message about the result and the HTTP Response
    '''
    id_value = request.args.get('id', '')
    return deleteHelper("book", "book_id", id_value)

@app.route('/author', methods=["DELETE"])
def deleteAuthor():
    '''
    Deletes an author based on the id given
    :return: A message about the result and the HTTP Response
    '''
    id_value = request.args.get('id', '')
    return deleteHelper("author", "author_id", id_value)

def deleteHelper(object, field, id_value):
    '''
    Helper function which takes in an id and deletes the object accordingly, if present
    :param object: the object which specifies which database to update
    :param field: the field which will tell MongoDB to search for either a book_id or a author_id
    :param id_value: the id value of the author or book
    :return: the message and the HTTP response
    '''
    result = docFromID(object, field, id_value)

    if result["HTTP Response"] == 200:
        db.get_collection(object).delete_one({field: int(id_value)})
        return "Deletion of " + object + " with id " + id_value + " successful", 200
    else:
        return result["Result"], result["HTTP Response"]

