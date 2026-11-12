# Expense Tracker Backend

A RESTful backend API for managing personal expenses, built with Python and FastAPI.

This project allows users to register, authenticate securely, and manage their personal expenses through REST API endpoints. It includes JWT-based authentication, user-specific data access, database migrations, and automated tests.

Built as a portfolio project to demonstrate backend development, API design, authentication, database management, and software testing.

## Features

- **User registration:** Create an account with email and password.
- **User authentication:** Secure login using JSON Web Tokens (JWT).
- **Password security:** Passwords are hashed before being stored.
- **Expense management:** Create, view, update, partially update, and delete expenses.
- **User-specific access:** Users can only access and manage their own expenses.
- **Input validation:** Reject invalid email addresses and non-positive expense amounts.
- **Database management:** SQLAlchemy ORM with Alembic database migrations.
- **Automated testing:** Tests covering authentication, expense operations, authorization, and validation.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- JWT Authentication
- Pytest
- Git and GitHub

## Project Structure

```text
expense-tracker-backend/
│
├── alembic/                 # Database migration files
├── app/
│   ├── api/
│   │   └── routes/          # Authentication and expense endpoints
│   ├── core/                # Configuration and security
│   ├── db/                  # Database connection and sessions
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic request and response schemas
│   └── main.py              # FastAPI application entry point
├── tests/                   # Automated tests
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Katlehodesigns/expense-tracker-backend.git
cd expense-tracker-backend
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory.

Add your own secret key:

```env
SECRET_KEY=your-secret-key
```

Never commit your actual `.env` file to GitHub.

### 6. Apply database migrations

```bash
alembic upgrade head
```

### 7. Start the development server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

Base URL: `http://127.0.0.1:8000`

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive an access token | No |
| GET | `/auth/me` | Retrieve authenticated user details | Yes |

### Expenses

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/expenses/` | Create an expense | Yes |
| GET | `/expenses/` | Retrieve the user's expenses | Yes |
| PUT | `/expenses/{expense_id}` | Fully update an expense | Yes |
| PATCH | `/expenses/{expense_id}` | Partially update an expense | Yes |
| DELETE | `/expenses/{expense_id}` | Delete an expense | Yes |

## Authentication

The API uses JSON Web Tokens (JWT) to authenticate users.

To access protected endpoints:

1. Register an account using `/auth/register`.
2. Log in using `/auth/login`.
3. Copy the returned access token.
4. Include the token in the Authorization header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Users can only access and manage their own expenses.

## Running Tests

This project uses **Pytest** for automated testing.

Run the test suite with:

```bash
python -m pytest -v
```

The tests cover:

- Root endpoint functionality.
- User registration and login.
- Password and authentication validation.
- JWT-protected endpoints.
- Expense creation and retrieval.
- Expense updates and deletion.
- User-specific access and authorization.
- Input validation, including invalid email addresses and non-positive expense amounts.

The project currently includes **23 automated tests**.