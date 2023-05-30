import json
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from sqlalchemy import func
from books_app import db, Book, Customer, Loan

app = Flask(__name__, template_folder='Front/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app)

db.init_app(app)

# home page
@app.route('/')
def index():
    return """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System</title>
    <!-- Add Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">
    <script src="https://cdn.jsdelivr.net/npm/axios@1.1.2/dist/axios.min.js"></script>
    <style>
        /* Adjust spacing */
        .container {
            display: flex;
            margin-top: 30px;
        }

        .left-section {
            flex: 1;
        }

        .right-section {
            flex: 1;
        }

        .show-buttons {
            display: flex;
            justify-content: flex-end;
            margin-right: 24%;
        }

        #overdue-books-container {
            position: absolute;
            top: 80px;
             right: 0;
            width: 300px;
            padding: 10px;
        }

        /* Adjust footer styles */
        footer {
            background-color: #f8f9fa;
            padding: 10px;
            text-align: center;
        }
    </style>
</head>

<body>
    <!-- Add Bootstrap navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="#">Library Management System</a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <button class="btn btn-primary mx-2" onclick="showBooks()">Show Books Data</button>
                </li>
                <li class="nav-item">
                    <button class="btn btn-primary mx-2" onclick="showCustomers()">Show Customers Data</button>
                </li>
                <li class="nav-item">
                    <button class="btn btn-primary mx-2" onclick="showLoans()">Show Loans Data</button>
                </li>
                <li class="nav-item">
                    <button class="btn btn-primary mx-2" id="show-overdue-books-btn">Show Overdue Books</button>
                  </li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <div class="left-section">
            <h1>Books</h1>
            <!-- Add new book form -->
            <h2>Add New Book</h2>
            Author: <input id="author"><br>
            Name: <input id="book_name"><br>
            Year: <input id="book_year"><br>
            Book Type:
            <select id="book_type">
                <option value="1">Type 1</option>
                <option value="2">Type 2</option>
                <option value="3">Type 3</option>
            </select><br>
            <button onclick="newBook()">Add New Book</button>

            <h1>Customers</h1>
            <!-- Add new customer form -->
            <h2>Add New Customer</h2>
            Name: <input id="cust_name"><br>
            City: <input id="cust_city"><br>
            Age: <input id="cust_age"><br>
            <button onclick="newCustomer()">Add New Customer</button>

            <h1>Loans</h1>
            <!-- Add new loan form -->
            <h2>Loan a new book</h2>
            Customer ID: <input id="loan_cust_id"><br>
            Book ID: <input id="loan_book_id"><br>
            <button onclick="newLoan()" id="loanBtn">Add New Loan</button>
            <div id="BooksSection">
                <h2>Search Books</h2>
                <input type="text" id="searchBookInput" placeholder="Enter book name">
                <button onclick="searchBooks()">Search</button>
                <div id="bookSearchResults"></div>
                <div id="Books" style="display: none;"></div>
            </div>
        
            <div id="CustomersSection">
                <h2>Search Customers</h2>
                <input type="text" id="searchCustomerInput" placeholder="Enter customer name">
                <button onclick="searchCustomers()">Search</button>
                <div id="customerSearchResults"></div>
                <div id="Customers" style="display: none;"></div>
              </div>
        
        </div>

        <div class="right-section">
            <div id="DataDisplay"></div>

            <div id="BooksSection">
                <div id="Books" style="display: none;"></div>
            </div>

            <div id="CustomersSection">
                <div id="Customers" style="display: none;"></div>
            </div>

            <div id="LoansSection">
                <div id="Loans" style="display: none;"></div>
            </div>
        </div>
    </div>
    <!-- Add Bootstrap JS and custom script -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/toastify-js"></script>
    <script src="script.js"></script>

    <!-- Add footer -->
    <footer>
        <p>&copy; 2023 Your Library Name. All rights reserved.</p>
    </footer>
</body>

</html>
"""

# get all books
@app.route("/books", methods=['GET'])
def get_books():
    books_list = [book.to_dict() for book in Book.query.all()]
    json_data = json.dumps(books_list)
    return json_data

# get a single book by its ID
@app.route("/books/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return {'error': 'Book not found'}, 404

    return book.to_dict()

# get all customers
@app.route("/customers", methods=['GET'])
def get_customers():
    customers_list = [customer.to_dict() for customer in Customer.query.all()]
    json_data = json.dumps(customers_list)
    return json_data

# get all loans
@app.route("/loans", methods=['GET'])
def get_loans():
    loans_list = [loan.to_dict() for loan in Loan.query.all()]
    json_data = json.dumps(loans_list)
    return json_data

# delete a book by its ID
@app.route("/books/del/<id>", methods=['DELETE'])
def del_book(id=-1):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return {"delete": "success"}

# delete a customer by their ID
@app.route("/customers/del/<id>", methods=['DELETE'])
def del_customer(id=-1):
    customer = Customer.query.get_or_404(id)

    # check if the customer has any loans
    if customer.loans:
        return {"error": "Cannot delete customer, since they have books loaned."}, 400

    # if the customer has no loans, delete them
    db.session.delete(customer)
    db.session.commit()
    return {"delete": "success"}

# delete a loan by its ID
@app.route("/loans/del/<id>", methods=['DELETE'])
def del_loan(id=-1):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    return {"delete": "success"}

# update a book by its ID
@app.route("/books/upd/<id>", methods=['PUT'])
def upd_book(id=-1):
    book = Book.query.get(id)
    data = request.get_json()
    book.book_author = data['book_author']
    book.book_name = data['book_name']
    book.book_year = data['book_year']
    book.book_type = data['book_type']
    db.session.commit()
    return {"update": "success"}

# update a customer by their ID
@app.route("/customers/upd/<id>", methods=['PUT'])
def upd_customer(id=-1):
    customer = Customer.query.get(id)
    data = request.get_json()
    customer.cust_name = data['cust_name']
    customer.cust_city = data['cust_city']
    customer.cust_age = data['cust_age']
    db.session.commit()
    return {"update": "success"}

# create a new book record
@app.route('/books/new', methods=['POST'])
def new_book():
    data = request.get_json()
    book_name = data['book_name']
    book_author = data['book_author']
    book_year = data['book_year']
    book_type = data['book_type']

    new_book = Book(book_name, book_author, book_year, book_type)
    db.session.add(new_book)
    db.session.commit()
    return "A new book record was created."

# create a new customer record
@app.route('/customers/new', methods=['POST'])
def new_customer():
    data = request.get_json()
    cust_name = data['cust_name']
    cust_city = data['cust_city']
    cust_age = data['cust_age']

    new_customer = Customer(cust_name, cust_city, cust_age)
    db.session.add(new_customer)
    db.session.commit()
    return "A new customer record was created."

# create a new loan record
@app.route('/loans/new', methods=['POST'])
def new_loan():
    data = request.get_json()
    cust_id = data['cust_id']
    book_id = data['book_id']
    book_type = str(data['book_type'])

    # Check if the book and customer exists
    book = Book.query.get(book_id)
    customer = Customer.query.get(cust_id)
    if customer is None:
        return {'error': 'Invalid ID'}, 400
    elif book is None: 
        return {'error': 'Invalid ID'}, 400
    

    # Check if the book is already loaned
    loaned_book = Loan.query.filter_by(book_id=book_id).first()
    if loaned_book is not None:
        return {'error': 'The book is already loaned'}, 400

    # Perform loan creation
    loanDate = datetime.now().strftime('%Y-%m-%d')
    if book_type == '1':
        returnDate = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    elif book_type == '2':
        returnDate = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    elif book_type == '3':
        returnDate = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    else:
        return {'error': 'Invalid book type'}, 400

    new_loan = Loan(cust_id, book_id, loanDate, returnDate)
    db.session.add(new_loan)
    db.session.commit()
    return "A new loan record was created."

# search for books by book name or author
@app.route('/books/search/<string:query>', methods=['GET'])
def search_books(query):
    # Convert the query to lowercase and add wildcards
    search_query = f'%{query.lower()}%'
    books_list = [book.to_dict() for book in Book.query.filter(func.lower(Book.book_name).like(search_query)).all()]
    json_data = json.dumps(books_list)
    return json_data

# search for customers by name
@app.route("/customers/search/<string:query>", methods=['GET'])
def search_customers(query):
    # Convert the query to lowercase and add wildcards
    search_query = f'%{query.lower()}%'
    customers_list = [customer.to_dict() for customer in Customer.query.filter(func.lower(Customer.cust_name).like(search_query)).all()]
    json_data = json.dumps(customers_list)
    return json_data

# get all overdue books based on return date
@app.route('/books-overdue', methods=['GET'])
def get_books_overdue():
    today = date.today().strftime('%Y-%m-%d')
    overdue_books = db.session.query(Book, Loan.returnDate, Loan.cust_id)\
                    .join(Loan, Book.id == Loan.book_id)\
                    .join(Customer, Loan.cust_id == Customer.id)\
                    .filter(Loan.returnDate < today)\
                    .all()

    books_list = []
    for book, returnDate, cust_id in overdue_books:
        book_dict = book.to_dict()
        book_dict['returnDate'] = returnDate
        book_dict['cust_id'] = cust_id
        book_dict['book_id'] = book.id    # add the book ID to the dictionary
        books_list.append(book_dict)

    json_data = json.dumps(books_list)
    return json_data

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
