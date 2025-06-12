from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from db_setup import db
from models import Author, Book, Category, Member, BorrowingRecord

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return "Library Management System API"


# Utility function for error handling
def get_or_404(model, id):
    instance = model.query.get(id)
    if not instance:
        abort(404, description=f"{model.__name__} with ID {id} not found")
    return instance

# GET routes with nested data and filtering
@app.route('/authors')
def get_authors():
    authors = Author.query.all()
    return jsonify([
        {
            'id': a.id,
            'name': a.name,
            'email': a.email,
            'bio': a.bio,
            'birth_date': a.birth_date,
            'books': [{'id': b.id, 'title': b.title} for b in a.books]
        } for a in authors
    ])

@app.route('/authors/<int:id>')
def get_author(id):
    author = get_or_404(Author, id)
    return jsonify({
        'id': author.id,
        'name': author.name,
        'email': author.email,
        'bio': author.bio,
        'birth_date': author.birth_date,
        'books': [{'id': b.id, 'title': b.title} for b in author.books]
    })

@app.route('/books')
def get_books():
    category_name = request.args.get('category')
    author_id = request.args.get('author_id')
    query = Book.query
    if category_name:
        query = query.join(Book.categories).filter(Category.name.ilike(f"%{category_name}%"))
    if author_id:
        query = query.filter(Book.author_id == author_id)
    books = query.all()
    return jsonify([
        {
            'id': b.id,
            'title': b.title,
            'isbn': b.isbn,
            'publication_date': b.publication_date,
            'page_count': b.page_count,
            'author': {
                'id': b.author.id,
                'name': b.author.name
            } if b.author else None,
            'categories': [{'id': c.id, 'name': c.name} for c in b.categories]
        } for b in books
    ])

@app.route('/books/<int:id>')
def get_book(id):
    book = get_or_404(Book, id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'isbn': book.isbn,
        'publication_date': book.publication_date,
        'page_count': book.page_count,
        'author': {
            'id': book.author.id,
            'name': book.author.name
        } if book.author else None,
        'categories': [{'id': c.id, 'name': c.name} for c in book.categories]
    })

@app.route('/categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in categories])

@app.route('/categories/<int:id>')
def get_category(id):
    category = get_or_404(Category, id)
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'books': [{'id': b.id, 'title': b.title} for b in category.books]
    })

@app.route('/members')
def get_members():
    members = Member.query.all()
    return jsonify([
        {
            'id': m.id,
            'name': m.name,
            'email': m.email,
            'phone': m.phone,
            'membership_date': m.membership_date,
            'borrowing_records': [{'id': r.id} for r in m.borrowing_records]
        } for m in members
    ])

@app.route('/members/<int:id>')
def get_member(id):
    member = get_or_404(Member, id)
    return jsonify({
        'id': member.id,
        'name': member.name,
        'email': member.email,
        'phone': member.phone,
        'membership_date': member.membership_date,
        'borrowing_records': [{'id': r.id} for r in member.borrowing_records]
    })

@app.route('/borrowing-records')
def get_borrowing_records():
    records = BorrowingRecord.query.all()
    return jsonify([
        {
            'id': r.id,
            'borrow_date': r.borrow_date,
            'return_date': r.return_date,
            'due_date': r.due_date,
            'book': {'id': r.book.id, 'title': r.book.title} if r.book else None,
            'member': {'id': r.member.id, 'name': r.member.name} if r.member else None
        } for r in records
    ])

@app.route('/borrowing-records/<int:id>')
def get_borrowing_record(id):
    r = get_or_404(BorrowingRecord, id)
    return jsonify({
        'id': r.id,
        'borrow_date': r.borrow_date,
        'return_date': r.return_date,
        'due_date': r.due_date,
        'book': {'id': r.book.id, 'title': r.book.title} if r.book else None,
        'member': {'id': r.member.id, 'name': r.member.name} if r.member else None
    })

# POST routes with basic validation
@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        abort(400, description='Missing required author fields')
    author = Author(name=data['name'], email=data['email'], bio=data.get('bio'), birth_date=data.get('birth_date'))
    db.session.add(author)
    db.session.commit()
    return jsonify({'message': 'Author created'}), 201

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not all(k in data for k in ('title', 'isbn', 'author_id')):
        abort(400, description='Missing required book fields')
    book = Book(
        title=data['title'],
        isbn=data['isbn'],
        publication_date=data.get('publication_date'),
        page_count=data.get('page_count'),
        author_id=data['author_id']
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book created'}), 201

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data.get('name'):
        abort(400, description='Missing category name')
    category = Category(name=data['name'], description=data.get('description'))
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created'}), 201

@app.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        abort(400, description='Missing required member fields')
    member = Member(name=data['name'], email=data['email'], phone=data.get('phone'), membership_date=data.get('membership_date'))
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Member created'}), 201

@app.route('/borrowing-records', methods=['POST'])
def create_borrowing_record():
    data = request.get_json()
    if not all(k in data for k in ('borrow_date', 'due_date', 'book_id', 'member_id')):
        abort(400, description='Missing required borrowing record fields')
    record = BorrowingRecord(
        borrow_date=data['borrow_date'],
        return_date=data.get('return_date'),
        due_date=data['due_date'],
        book_id=data['book_id'],
        member_id=data['member_id']
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Borrowing record created'}), 201

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)
