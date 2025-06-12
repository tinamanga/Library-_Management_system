from db_setup import db

# Author can write many books
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    bio = db.Column(db.Text)
    birth_date = db.Column(db.String(20))
    books = db.relationship('Book', backref='author')

# Books can belong to many categories
book_category = db.Table('book_category',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    isbn = db.Column(db.String(20))
    publication_date = db.Column(db.String(20))
    page_count = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    categories = db.relationship('Category', secondary=book_category, backref='books')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))

# Members can have many borrowing records
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    membership_date = db.Column(db.String(20))
    borrowing_records = db.relationship('BorrowingRecord', backref='member')

class BorrowingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.String(20))
    return_date = db.Column(db.String(20))
    due_date = db.Column(db.String(20))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
