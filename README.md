# flask-server

Require flask and psycopg2 python libraries. Tested in Python3. 

Establish a Postgres server on port 1234, and set up a table called "template1". Install a db user "postgres". Test application is hosted on port 5000. 

### NOTE: 
Currently exiting the application does not delete the tables by default so all records are persisted. Uncomment the line in main to enable clean up of the db after exiting the application. 


## APIs

All requests are served using json inputs, except the ones used to observe the state of the db (getAllUsers, getAllBooks, getAllTransactions, which takes no parameters).

Request urls:
- /api/v1.0/users, supports GET and POST for getting and inserting users
- /api/v1.0/books, supports GET and POST for getting and inserting books
- /api/v1.0/transactions, supports POST and PUT, for inserting and updating transactions (borrowing of books) 

Example:

`curl --header "Content-Type: application/json" --request POST --data '{"firstName":"john", "lastName":"dee", "bookName":"john"}' http://localhost:5000/api/v1.0/transactions` 

Tries to insert a transaction into the db, fails if the users / book does not exist 


## TODOs:

- config parsing 
- testing suite
- asynchronous processing 
- user authentication 
- etc. 

