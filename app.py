from flask import Flask, request, jsonify
from db_setup import db
from models import Author, Book, Category, Member, BorrowingRecord
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    return "Library Management System API"

# GET routes
@app.route('/authors')
def get_authors():
    authors = Author.query.all()
    return jsonify([{'id': a.id, 'name': a.name, 'email': a.email} for a in authors])

@app.route('/authors/<int:id>')
def get_author(id):
    author = Author.query.get_or_404(id)
    return jsonify({'id': author.id, 'name': author.name, 'email': author.email, 'bio': author.bio, 'birth_date': author.birth_date})

@app.route('/books')
def get_books():
    books = Book.query.all()
    return jsonify([{'id': b.id, 'title': b.title, 'isbn': b.isbn} for b in books])

@app.route('/books/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({'id': book.id, 'title': book.title, 'isbn': book.isbn, 'author': book.author.name if book.author else None})

@app.route('/categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

@app.route('/categories/<int:id>')
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify({'id': category.id, 'name': category.name, 'description': category.description})

@app.route('/members')
def get_members():
    members = Member.query.all()
    return jsonify([{'id': m.id, 'name': m.name} for m in members])

@app.route('/members/<int:id>')
def get_member(id):
    member = Member.query.get_or_404(id)
    return jsonify({'id': member.id, 'name': member.name, 'email': member.email})

@app.route('/borrowing-records')
def get_borrowing_records():
    records = BorrowingRecord.query.all()
    return jsonify([{'id': r.id, 'book_id': r.book_id, 'member_id': r.member_id} for r in records])

@app.route('/borrowing-records/<int:id>')
def get_borrowing_record(id):
    record = BorrowingRecord.query.get_or_404(id)
    return jsonify({'id': record.id, 'borrow_date': record.borrow_date, 'due_date': record.due_date, 'return_date': record.return_date})

# POST routes
@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    author = Author(name=data['name'], email=data['email'], bio=data['bio'], birth_date=data['birth_date'])
    db.session.add(author)
    db.session.commit()
    return jsonify({'message': 'Author created'}), 201

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book(title=data['title'], isbn=data['isbn'], publication_date=data['publication_date'], page_count=data['page_count'], author_id=data['author_id'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book created'}), 201

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category = Category(name=data['name'], description=data['description'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created'}), 201

@app.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()
    member = Member(name=data['name'], email=data['email'], phone=data['phone'], membership_date=data['membership_date'])
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Member created'}), 201

@app.route('/borrowing-records', methods=['POST'])
def create_borrowing_record():
    data = request.get_json()
    record = BorrowingRecord(borrow_date=data['borrow_date'], return_date=data['return_date'], due_date=data['due_date'], book_id=data['book_id'], member_id=data['member_id'])
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Borrowing record created'}), 201

if __name__ == '__main__':
    app.run(debug=True)
