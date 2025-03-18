# FastAPI Application

This is a FastAPI-based application.

## Prerequisites

Make sure you have the following installed:
- Python 3.9+
- pip
- Docker

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/fastapi-app.git
   cd fastapi-app
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Using Docker Compose

1. Ensure you have Docker and Docker Compose installed.
2. Start the application using Docker Compose:
```bash
docker-compose up --build
```
3. The application doc will be available at:
- [http://127.0.0.1:8000](http://127.0.0.1:8000)
- OpenAPI documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Database Migrations with Alembic
Alembic is used for database migrations.
Apply migrations using:
```bash
alembic upgrade head
```

If needed, you can downgrade to the previous version:
## Running Tests

Run the test suite using `pytest`:
```bash
pytest
```

To check code coverage:
```bash
pytest --cov=app
```

# Environment Variables
Create a .env file in the root directory and add required environment as in .env.sample.