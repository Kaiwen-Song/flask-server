class Api(object):
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
            response = requesthandler.get_user(db_accessor, first_name, last_name)
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
            resp = requesthandler.add_user(db_accessor, first_name, last_name)
            return jsonify({"addUser" : {}})
        except Exception as e:
            return response

    @app.route('/api/v1.0/books', methods=['POST'])
    def add_book():
        if not request.json:
            abort(400)
        if "bookName" not in request.json or "authorName" not in request.json:
            abort(402)
        try:
            book_name = request.json["bookName"]
            author_name = request.json["authorName"]
            resp = requesthandler.add_book(db_accessor, book_name, author_name)
            return jsonify({"addBook" : {}})
        except Exception as e:
            return jsonify({})        

    @app.route('/api/v1.0/books', methods=['GET'])
    def get_books():
        if not request.json:
            abort(400)
        if "bookName" not in request.json and "authorName" not in request.json:
            abort(402)
        try:
            book_name = request.json["bookName"]
            author_name = request.json["authorName"]
            resp = requesthandler.get_book(db_accessor, book_name, author_name)
            return jsonify({"getBook" : resp})
        except Exception as e:
            return jsonify({})
        
    @app.route('/api/v1.0/activities', methods=['POST'])
    def borrow_book():
        return jsonify({})

    @app.route('/api/v1.0/allusers', methods=["GET"])
    def get_all_users():
        return jsonify({"users" : db_accessor.get_all_users()})

    @app.route('/api/v1.0/allbooks', methods=["GET"])
    def get_all_books():
        return jsonify({"books" : db_accessor.get_all_books()})

    @app.route('/api/v1.0/alltransactions', methods=["GET"])
    def get_all_transactions():
        return jsonify({"transactions" : db_accessor.get_all_transactions()})
