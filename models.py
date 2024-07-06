from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text, nullable=True)

    reviews = db.relationship('Review', backref='book', lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(100), primary_key=True)
    book_id = db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.String(100),nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
