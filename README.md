# cspsc449-hw2
CPSC 449
Homework-2
Web backend engineering
Problem statement:
Implement a “book management system” using FAST API and connect to MySQL database
Thing to be done:
1) The number of data fields if left to your wish
2) Comment down each line of your code explaining its use.
3) Make use of pydantic models for validation
4) submit your code in GitHub and submit the link along with video recording

# Book Management System - Backend

## Setup and Running

### Prerequisites
- Docker
- Docker Compose
- Create .env file
```
MYSQL_DATABASE_URL=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@db:3306/book_management

MYSQL_ROOT_PASSWORD=password    #Replace with your MySQL credentials
```

### Installation Steps
1. Clone the repository
2. Run `docker-compose up --build`

### API Endpoints
- `POST /books/`: Create a new book
- `GET /books/`: List all books
- `GET /books/{book_id}`: Get a specific book
- `PUT /books/{book_id}`: Update a book
- `DELETE /books/{book_id}`: Delete a book