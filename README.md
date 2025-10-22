# Todo API

A simple and efficient Todo API built with FastAPI, SQLAlchemy, and PostgreSQL/SQLite.

## Features

- ✅ Create, read, update, and delete todos
- ✅ Search todos by title and description
- ✅ Filter todos by completion status
- ✅ Pagination support
- ✅ Toggle todo completion status
- ✅ Comprehensive error handling
- ✅ CORS support for frontend integration
- ✅ Automatic API documentation
- ✅ Database migrations support

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL/SQLite** - Database
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dump_project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env_example.txt .env
# Edit .env with your database configuration
```

## Database Setup

### SQLite (Default - Recommended)
No additional setup required! The app uses SQLite by default and will automatically create a `todoapp.db` file in your project directory.

### PostgreSQL (Optional)
If you prefer PostgreSQL for production:
1. Install PostgreSQL
2. Create a database:
```sql
CREATE DATABASE todoapp;
```
3. Update the `DATABASE_URL` in your `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
```

## Running the Application

1. Start the development server:
```bash
uvicorn main:app --reload
```

2. The API will be available at:
   - **API**: http://localhost:8000
   - **Interactive Docs**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Todos

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/todos/` | Get all todos with pagination and filtering |
| POST | `/api/v1/todos/` | Create a new todo |
| GET | `/api/v1/todos/{id}` | Get a specific todo |
| PUT | `/api/v1/todos/{id}` | Update a todo |
| PATCH | `/api/v1/todos/{id}/toggle` | Toggle todo completion status |
| DELETE | `/api/v1/todos/{id}` | Delete a todo |

### Query Parameters

- `page` (int): Page number (default: 1)
- `size` (int): Items per page (default: 10, max: 100)
- `search` (string): Search in title and description
- `is_completed` (boolean): Filter by completion status

### Example Requests

#### Create a Todo
```bash
curl -X POST "http://localhost:8000/api/v1/todos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "is_completed": false
  }'
```

#### Get All Todos
```bash
curl "http://localhost:8000/api/v1/todos/?page=1&size=10&search=FastAPI"
```

#### Update a Todo
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI - Updated",
    "is_completed": true
  }'
```

#### Toggle Todo Completion
```bash
curl -X PATCH "http://localhost:8000/api/v1/todos/1/toggle"
```

## Project Structure

```
dump_project/
├── app/
│   ├── __init__.py
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   ├── exceptions.py        # Custom exception handlers
│   └── routers/
│       ├── __init__.py
│       └── todos.py         # Todo endpoints
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── env_example.txt         # Environment variables example
└── README.md               # This file
```

## Development

### Adding New Features

1. Create new models in `app/models.py`
2. Add corresponding schemas in `app/schemas.py`
3. Implement CRUD operations in `app/crud.py`
4. Create router endpoints in `app/routers/`
5. Update the main application in `main.py`

### Database Migrations

For production use, consider using Alembic for database migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
