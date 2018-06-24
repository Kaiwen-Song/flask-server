import psycopg2 as pg
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class DatabaseAccessor(object):

    def __init__(self, db_name, db_user, port):
        self._db_name = db_name
        self._db_user = db_user
        self._port = port

    @contextmanager
    def _get_db_connection(self):
        connection = pg.connect(database=self._db_name, user=self._db_user, port=self._port)
        cursor = connection.cursor()
        try:
            yield (connection, cursor)
        except Exception as e:
            logger.exception(e)
        finally:
            cursor.close()
            connection.close()


    def setup_table(self):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("""
                create table Users (
                    userId       serial PRIMARY KEY,
                    firstName    varchar(100) NOT NULL,
                    lastName     varchar(100) NOT NULL,
                    dateJoined   timestamp default current_timestamp
                );""")
                
            cursor.execute("""
                create table Books (
                    bookId       serial PRIMARY KEY,
                    bookName     varchar(100) NOT NULL,
                    authorName   varchar(100) NOT NULL,
                    isAvailable   boolean default True
                );""")

            cursor.execute("""
                create table Transactions (
                    transactionId   serial PRIMARY KEY,
                    userId          integer REFERENCES Users (userId),
                    bookId          integer REFERENCES Books (bookId),
                    dateCreated   timestamp default current_timestamp,
                    dateCompleted   timestamp
                );""")

            connection.commit()
            logger.info("created tables")

    def cleanup_tables(self):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("DROP TABLE Transactions;")
            cursor.execute("DROP TABLE Users;")
            cursor.execute("DROP TABLE Books;")
            connection.commit()
            logger.info("dropped tables")

    
    def get_user_by_name(self, first_name, last_name):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("SELECT * FROM Users WHERE firstName=%s AND lastName=%s", (first_name, last_name, ))
            data = [{
                "userId" : row[0],
                "firstName" : row[1],
                "lastName" : row[2]
            } for row in cursor.fetchall()]
            print(data)
            return data


    def get_books_by_name(self, book_name, author_name = None):
        with self._get_db_connection() as (connection, cursor):
            if author_name:
                cursor.execute("SELECT * FROM Books WHERE bookName=%s AND authorName=%s", (book_name, author_name,))
            else:
                cursor.execute("SELECT * FROM Books WHERE bookName=%s", (book_name,))
            data = [{
                "bookId" : row[0],
                "bookName" : row[1],
                "authorName": row[2],
                "isAvailable" : row[3]
            } for row in cursor.fetchall()]
            print(data)
            return data


    def get_books_by_author(self, author_name):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("SELECT * FROM Books WHERE authorName=%s", (author_name, ))
            data = [{
                "bookId" : row[0],
                "bookName" : row[1],
                "authorName": row[2],
                "isAvailable" : row[3]
            } for row in cursor.fetchall()]
            return data


    def add_book(self, book_name, author_name):
        with self._get_db_connection() as (connection, cursor):
            query = "INSERT INTO Books(bookName, authorName) VALUES (%s, %s)"
            cursor.execute(query, (book_name, author_name, ))
            connection.commit()
            logger.info("Added book {} by {}".format(book_name, author_name))


    def add_user(self,first_name, last_name):
        with self._get_db_connection() as (connection, cursor):
            query = "INSERT INTO Users(firstName, lastName) VALUES (%s, %s)"
            cursor.execute(query, (first_name, last_name, ))
            connection.commit()
            logger.info("Added user {} {}".format(first_name, last_name))


    def borrow_book(self, user_id, book_id):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("UPDATE Books SET isAvailable = FALSE WHERE bookId = %s", (book_id, ))
            cursor.execute("INSERT INTO Transactions(userId, bookId) VALUES (%s, %s)", (user_id, book_id))
            connection.commit()
            return {"userId" : user_id, "bookId" : book_id}

    def return_book(self, book_id, transaction_id):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("UPDATE Books SET isAvailable = TRUE WHERE bookId = %s", (book_id, ))
            cursor.execute("UPDATE Transactions SET dateCompleted = NOW() WHERE transactionId = %s", 
                           (transaction_id, ))
            connection.commit()
    
    def get_transaction(self, user_id, book_id):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("SELECT * FROM Transactions WHERE bookId = %s AND userId = %s", (book_id, user_id,))
            data = [{
                "transactionId" : row[0],
                "userId" : row[1],
                "bookId" : row[2],
                "dateCreated" : row[3],
                "dateCompleted" : row[4]
            } for row in cursor.fetchall()]
            print(data)
            return data

    def get_all_users(self):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("SELECT * FROM Users;")
            data = [{
                "userId" : row[0],
                "firstName" : row[1],
                "lastName" : row[2]
            } for row in cursor.fetchall()]
            print(data)
            return data


    def get_all_books(self):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("SELECT * FROM Books;")
            data = [{
                "bookId" : row[0],
                "bookName" : row[1],
                "authorName": row[2],
                "isAvailable" : row[3]
            } for row in cursor.fetchall()]
            print(data)
            return data


    def get_all_transactions(self):
        with self._get_db_connection() as (connection, cursor):
            cursor.execute("SELECT * FROM Transactions;")
            data = [{
                "transactionId" : row[0],
                "userId" : row[1],
                "bookId" : row[2],
                "dateCreated" : row[3],
                "dateCompleted" : row[4]
            } for row in cursor.fetchall()]
            print(data)
            return data
