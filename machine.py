
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from models import Book, Review  # Import your SQLAlchemy models
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


# PostgreSQL connection string
connection_string = os.getenv('DATABASE_URI')

# Create an engine and a session
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
session = Session()

# Query the Book and Review data
books_query = session.query(Book).all()
reviews_query = session.query(Review).all()

# Convert the Book query results to a pandas DataFrame
books_data = [{
    'id': book.id,
    'title': book.title,
    'author': book.author,
    'genre': book.genre,
    'year_published': book.year_published
} for book in books_query]

books_df = pd.DataFrame(books_data)

# Convert the Review query results to a DataFrame
reviews_data = [{
    'id': review.id,
    'book_id': review.book_id,
    'user_id': review.user_id,
    'review_text': review.review_text,
    'rating': review.rating
} for review in reviews_query]

reviews_df = pd.DataFrame(reviews_data)

# Merge books_df with reviews_df to include average ratings
average_ratings = reviews_df.groupby('book_id')['rating'].mean().reset_index()
average_ratings.columns = ['id', 'Average-Rating']
books_df = books_df.merge(average_ratings, on='id', how='left').fillna(0)

# Preprocess data
books_df['title'] = books_df['title'].fillna('')
books_df['genre'] = books_df['genre'].fillna('')

# Concatenate title and genre for each book (you can extend this to other relevant features)
books_df['Combined-Features'] = books_df['title'] + ' ' + books_df['genre']

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the TF-IDF vectorizer
tfidf_matrix = tfidf_vectorizer.fit_transform(books_df['Combined-Features'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend books based on user input and rating
def recommend_books(user_input, min_rating):
    # Transform user input into TF-IDF vector
    user_tfidf = tfidf_vectorizer.transform([user_input])

    # Calculate cosine similarity between user input and all books
    similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix).flatten()

    # Sort indices based on similarity scores
    sorted_indices = similarity_scores.argsort()[::-1]

    # Filter books by minimum rating
    recommended_books = books_df.iloc[sorted_indices]
    recommended_books = recommended_books[recommended_books['Average-Rating'] >= min_rating]

    if recommended_books.empty:
        return "No books found matching the given criteria."

    # Use a set to track unique book IDs
    unique_books = set()
    recommended_details = []

    # Get detailed information for the top 10 most similar books meeting the rating requirement
    for index, row in recommended_books.iterrows():
        if row['id'] not in unique_books:
            unique_books.add(row['id'])
            details = {
                'id': row['id'],
                'title': row['title'],
                'author': row['author'],
                'genre': row['genre'],
                'year_published': row['year_published'],
                'rating': row['Average-Rating']
            }
            recommended_details.append(details)
        if len(recommended_details) >= 10:
            break

    return recommended_details





