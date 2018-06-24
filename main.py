#!flask/bin/python
import sys
from flask import Flask, request, jsonify, abort, make_response
from dbaccessor import DatabaseAccessor
import requesthandler
import atexit
import logging
from statuscodes import StatusCode

DATABASE_NAME = "template1"
DATABASE_USER = "postgres"
PORT = 1234

logger = logging.getLogger(__name__)
app = Flask(__name__)
@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    if not request.json:
        abort(400)
    if "firstName" not in request.json or "lastName" not in request.json:
        abort(402)
    try:
        first_name = request.json["firstName"]
        last_name = request.json["lastName"]
        (status, resp) = requesthandler.get_user(db_accessor, first_name, last_name)
        return jsonify({"getUser": resp})
    except Exception as e:
        return jsonify({})

@app.route('/api/v1.0/users', methods=['POST'])
def insert_user():
    if not request.json:
        abort(400)
    if "firstName" not in request.json or "lastName" not in request.json:
        abort(402)
    try:
        first_name = request.json["firstName"]
        last_name = request.json["lastName"]
        (status, resp) = requesthandler.add_user(db_accessor, first_name, last_name)
        return make_response(jsonify({"addUser" : {}}), 201)
    except Exception as e:
        logger.exception()
        return make_response(jsonify({"error": "unable to add user"}),500)

@app.route('/api/v1.0/books', methods=['POST'])
def add_book():
    if not request.json or "bookName" not in request.json or "authorName" not in request.json:
        abort(400)
    try:
        book_name = request.json["bookName"]
        author_name = request.json["authorName"]
        (status, resp) = requesthandler.add_book(db_accessor, book_name, author_name)
        if status != StatusCode.SUCCESS:
            return make_response(jsonify({"error": "unknown error has occurred"}), 500)
        return make_response(jsonify({"addBook" : {}}), 201)
    except Exception as e:
        logger.exception(e)
        return jsonify({"error" : "unable to add book"})

@app.route('/api/v1.0/books', methods=['GET'])
def get_books():
    if not request.json or "bookName" not in request.json and "authorName" not in request.json:
        abort(400)
    try:
        book_name = request.json.get("bookName")
        author_name = request.json.get("authorName")
        (status, resp) = requesthandler.get_book(db_accessor, book_name, author_name)
        if status != StatusCode.SUCCESS:
            return jsonify({})
        return jsonify({"getBook" : resp})
    except Exception as e:
        logger.exception(e)
        return make_response(jsonify({"error" : "failed to retrieve books"}), 500)
    

@app.route('/api/v1.0/transactions', methods=['POST'])
def borrow_book():
    if (not request.json or 
        "bookName" not in request.json or "firstName" not in request.json
        or "lastName" not in request.json):
        abort(400)
    try:
        book_name = request.json.get("bookName")
        first_name = request.json.get("firstName")
        last_name = request.json.get("lastName")
        author_name = request.json.get("authorName")
        (status, resp) = requesthandler.borrow_book(db_accessor, first_name, last_name, book_name, author_name)
        if status != StatusCode.SUCCESS:
            return jsonify({{}})
        return make_response(jsonify({"borrowBook" : {}}), 201)
    except Exception as e:
        logger.exception(e)
        return make_response(jsonify({"borrowBook" : {}}), 500)


@app.route('/api/v1.0/transactions', methods=['PUT'])
def return_book():
    if (not request.json or 
        "bookId" not in request.json or "userId" not in request.json):
        abort(400)
    try:
        book_id = request.json.get("bookId")
        user_id = request.json.get("userId")
        (status, resp) = requesthandler.return_book(db_accessor, user_id, book_id)
        if status != StatusCode.SUCCESS:
            return make_response(jsonify({"error": "Unable to return book"}), 500)
        return make_response(jsonify({"returnBook" : {}}), 200)
    except Exception as e:
        logger.exception(e)
        return make_response(jsonify({"error": "Unable to return book"}), 500)



@app.route('/api/v1.0/allusers', methods=["GET"])
def get_all_users():
    return jsonify({"users" : db_accessor.get_all_users()})

@app.route('/api/v1.0/allbooks', methods=["GET"])
def get_all_books():
    return jsonify({"books" : db_accessor.get_all_books()})

@app.route('/api/v1.0/alltransactions', methods=["GET"])
def get_all_transactions():
    return jsonify({"transactions" : db_accessor.get_all_transactions()})


if __name__ == '__main__':
    db_accessor = DatabaseAccessor(DATABASE_NAME, DATABASE_USER, PORT)
    db_accessor.setup_table()
    # atexit.register(db_accessor.cleanup_tables)
    app.run(debug=True)