from flask import Flask, request, jsonify
from flasgger import Swagger
from models import db, Book, Review
from config import Config
from werkzeug.utils import secure_filename
from summary import map_reduce
from machine import recommend_books
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

swagger = Swagger(app, template_file=os.getenv("SWAGGER_FILE_PATH"))

with app.app_context():
    db.create_all()

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        id = data['id'],
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        year_published=data['year_published'],
        summary=data.get('summary')
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'year_published': book.year_published,
        'summary': book.summary
    } for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'year_published': book.year_published,
        'summary': book.summary
    })

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.year_published = data.get('year_published', book.year_published)
    book.summary = data.get('summary', book.summary)
    db.session.commit()
    return jsonify({"message": "Book updated successfully!"})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"})

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    new_review = Review(
        id = data['id'],
        book_id=data['book_id'],
        user_id=data['user_id'],
        review_text=data['review_text'],
        rating=data['rating']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review added successfully!"}), 201

@app.route('/books/<int:book_id>/reviews', methods=['GET'])
def get_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    return jsonify([{
        'id': review.id,
        'book_id': review.book_id,
        'user_id': review.user_id,
        'review_text': review.review_text,
        'rating': review.rating
    } for review in reviews])

@app.route('/books/<int:book_id>/summary', methods=['GET'])
def get_book_summary(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        avg_rating = None
    return jsonify({
        'summary': book.summary,
        'average_rating': avg_rating
    })

@app.route('/books/<int:id>/summary', methods=['PUT'])
def update_summary(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)
        
        summary = map_reduce(file_path)
        os.remove(file_path)



    book.summary = summary
    db.session.commit()
    
    return jsonify({'message': 'Summary updated successfully'}), 200

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)
        
        summary = map_reduce(file_path)
        os.remove(file_path)
        
        return jsonify({"summary": summary})



# Route for book recommendation
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_input = data['user_input']
    min_rating = float(data['min_rating'])

    recommended_books = recommend_books(user_input, min_rating)

    return jsonify({
        'recommended_books': recommended_books
    })

    # if isinstance(recommended_books, list):
    #     return render_template('recommendations.html', books=recommended_books, user_input=user_input, min_rating=min_rating)
    # else:
    #     return render_template('error.html', message=recommended_books)




if __name__ == '__main__':

    app.run(debug=True, port=os.getenv("PORT"))