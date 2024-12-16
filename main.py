# Importing necessary modules from FastAPI, Pydantic, SQLAlchemy, and Python's typing library
from fastapi import Depends, FastAPI, HTTPException  # FastAPI framework and dependencies management
from pydantic import BaseModel  # BaseModel for data validation and serialization
from typing import List  # List for type hinting in response models
from sqlalchemy import create_engine, Column, Integer, String  # SQLAlchemy utilities for ORM mapping
from sqlalchemy.ext.declarative import declarative_base  # Base class for SQLAlchemy models
from sqlalchemy.orm import sessionmaker, Session  # Session and sessionmaker for database interactions

# SQLAlchemy configuration
DATABASE_URL = "mysql+pymysql://root:password@db/book_management"  # MySQL database connection string
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})  # Create SQLAlchemy engine with utf8mb4 charset
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Create a session factory for database sessions
Base = declarative_base()  # Base class for defining SQLAlchemy ORM models

# SQLAlchemy model for Book
class Book(Base):
    """
    Represents the 'books' table in the database.
    """
    __tablename__ = "books"  # Table name in the database
    id = Column(Integer, primary_key=True, index=True)  # Primary key column with indexing for fast lookups
    title = Column(String(255), nullable=False)  # Title of the book (required field, max 255 characters)
    author = Column(String(255), nullable=False)  # Author of the book (required field, max 255 characters)
    published_year = Column(Integer, nullable=False)  # Year the book was published (required field)
    genre = Column(String(100), nullable=False)  # Genre of the book (required field, max 100 characters)
    description = Column(String(500))  # Description of the book (optional field, max 500 characters)

# Pydantic model for Book input validation
class BookCreate(BaseModel):
    """
    Schema for validating book input data.
    """
    title: str  # Title of the book
    author: str  # Author of the book
    published_year: int  # Year the book was published
    genre: str  # Genre of the book
    description: str = None  # Optional description of the book

class BookOut(BookCreate):
    """
    Schema for output data, includes book ID.
    """
    id: int  # Unique identifier for the book

    class Config:
        orm_mode = True  # Allows automatic conversion of ORM objects to dictionaries

# Initialize FastAPI app
app = FastAPI()  # Create a FastAPI application instance

# Dependency to get DB session
def get_db():
    """
    Provides a database session for each request.
    """
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to be used by the request
    finally:
        db.close()  # Ensure the session is closed after the request

# Create database tables
Base.metadata.create_all(bind=engine)  # Automatically create tables defined in SQLAlchemy models

# Routes
@app.get("/books", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    """
    Retrieve all books from the database.
    """
    books = db.query(Book).all()  # Fetch all book records
    return books  # Return the list of books

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific book by ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()  # Fetch the book with the given ID
    if not book:  # If the book doesn't exist, raise a 404 error
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # Return the book details

@app.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book entry in the database.
    """
    db_book = Book(
        title=book.title,
        author=book.author,
        published_year=book.published_year,
        genre=book.genre,
        description=book.description,
    )  # Map input data to SQLAlchemy model
    db.add(db_book)  # Add the new book to the session
    db.commit()  # Commit the transaction to save the book
    db.refresh(db_book)  # Refresh the instance to reflect changes (e.g., assigned ID)
    return db_book  # Return the created book

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    """
    Update an existing book's details in the database.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()  # Fetch the book with the given ID
    if not db_book:  # If the book doesn't exist, raise a 404 error
        raise HTTPException(status_code=404, detail="Book not found")
    # Update the book's details
    db_book.title = updated_book.title
    db_book.author = updated_book.author
    db_book.published_year = updated_book.published_year
    db_book.genre = updated_book.genre
    db_book.description = updated_book.description
    db.commit()  # Commit the changes
    db.refresh(db_book)  # Refresh the instance to reflect updated data
    return db_book  # Return the updated book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by ID from the database.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()  # Fetch the book with the given ID
    if not db_book:  # If the book doesn't exist, raise a 404 error
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)  # Delete the book from the session
    db.commit()  # Commit the transaction to apply the deletion
    return {"message": f"Book with ID {book_id} deleted"}  # Return a success message