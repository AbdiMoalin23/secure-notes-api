# Secure Notes API
A RESTful API built with FastAPI for securely managing personal notes with user authentication and protected routes. 

## Tech Stack
* Python
* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication
* Pydantic

## Features
* User Authentication & Login
* Password hashing with bcrypt
* JWT Authentication
* Create, read, update, and delete notes
* Mark notes as favourite 

## Setup & Installation
1. Clone the repository:
git clone https://github.com/AbdiMoalin23/secure-notes-api.git
cd secure-notes-api

Create a virtual environment:
python -m venv venv

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Run the server:
uvicorn app.main:app --reload

## API Usage

Open Swagger UI: http://127.0.0.1:8000/docs

Authentication Flow:
1. Register a user
2. Login
3. Click Authorize in Swagger
4. Enter your email as the username and your password

Access the protected note endpoints

Auth
    POST /register → Create a user
    POST /login → Get an access token
    GET /users/me → Get current user

Notes (Protected)
    POST /notes → Create a note
    GET /notes → Get all notes for current user
    GET /notes/{id} → Get a single note
    PUT /notes/{id} → Update a note
    DELETE /notes/{id} → Delete a note

## Project Structure
```
secure-notes-api
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routes/
│       ├── users.py
│       └── notes.py
│
├── requirements.txt
└── README.md
```
