import logging 
from statuscodes import StatusCode

logger = logging.getLogger(__name__)

def get_user(db_accessor, first_name, last_name):
    try: 
        return (StatusCode.SUCCESS, db_accessor.get_user_by_name(first_name, last_name))
    except Exception as e:
        logger.warn("Failed to retrieve users")
        return (StatusCode.ERROR, {})


def add_user(db_accessor, first_name, last_name):

    try:
        db_accessor.add_user(first_name, last_name)        
        return (StatusCode.SUCCESS, {})
    except Exception as e:
        logger.warn("Failed to add user")
        logger.exception(e)
        return (StatusCode.ERROR, {})

def get_book(db_accessor, book_name = None, author_name = None):
    try:
        if book_name:
            return (StatusCode.SUCCESS, db_accessor.get_books_by_name(book_name, author_name))
        else: 
            return (StatusCode.SUCCESS, db_accessor.get_books_by_author(author_name))
    except Exception as e:
        logger.exception(e)
        return (StatusCode.ERROR, {})

def add_book(db_accessor, book_name, author_name):
    try:
        return (StatusCode.SUCCESS, db_accessor.add_book(book_name, author_name))
    except Exception as e:
        logger.exception(e)
        return (StatusCode.ERROR, {})


def borrow_book(db_accessor, first_name, last_name, book_name, author_name=None):
    try:
        users = db_accessor.get_user_by_name(first_name, last_name)
        if len(users) < 1:
            raise Exception("no users matching the name entered")
        books = [book for book in db_accessor.get_books_by_name(book_name, author_name) if book["isAvailable"]]
        if len(books) < 1:
            raise Exception("no available books matching the name entered")
        book_id = books[0]['bookId']
        user_id = users[0]['userId']
        return (StatusCode.SUCCESS, db_accessor.borrow_book(user_id, book_id))
    except Exception as e:
        logger.exception(e)
        return (StatusCode.ERROR, {})

def return_book(db_accessor, user_id, book_id):
    try:
        transactions = [transaction 
                        for transaction in db_accessor.get_transaction(user_id, book_id) 
                        if not transaction['dateCompleted']]
        if len(transactions) < 1:
            raise Exception("no pending transaction")
        transaction_id = transactions[0]["transactionId"]
        return (StatusCode.SUCCESS, db_accessor.return_book(book_id, transaction_id))
    except Exception as e:
        logger.exception(e)
        return (StatusCode.ERROR, {})
