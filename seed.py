from faker import Faker
from app import db, app
from models import Author, Book, Category, Member, BorrowingRecord
import random

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Seed Authors
    authors = []
    for _ in range(20):
        author = Author(
            name=fake.name(),
            email=fake.email(),
            bio=fake.text(),
            birth_date=fake.date_of_birth().strftime('%Y-%m-%d')
        )
        db.session.add(author)
        authors.append(author)

    # Seed Categories
    categories = []
    for _ in range(10):
        category = Category(
            name=fake.word(),
            description=fake.text()
        )
        db.session.add(category)
        categories.append(category)

    db.session.commit()

    # Seed Books
    books = []
    for _ in range(20):
        book = Book(
            title=fake.sentence(nb_words=3),
            isbn=fake.isbn13(),
            publication_date=fake.date_this_century().strftime('%Y-%m-%d'),
            page_count=random.randint(100, 500),
            author=random.choice(authors)
        )
        # Assign 1–3 categories to each book
        book.categories = random.sample(categories, k=random.randint(1, 3))
        db.session.add(book)
        books.append(book)

    # Seed Members
    members = []
    for _ in range(20):
        member = Member(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            membership_date=fake.date_this_decade().strftime('%Y-%m-%d')
        )
        db.session.add(member)
        members.append(member)

    db.session.commit()

    # Seed Borrowing Records
    for _ in range(20):
        record = BorrowingRecord(
            borrow_date=fake.date_this_year().strftime('%Y-%m-%d'),
            return_date=fake.date_this_year().strftime('%Y-%m-%d'),
            due_date=fake.date_this_year().strftime('%Y-%m-%d'),
            book_id=random.choice(books).id,
            member_id=random.choice(members).id
        )
        db.session.add(record)

    db.session.commit()
    print(" Database seeded with authors, books, categories, members, and borrowing records!")
