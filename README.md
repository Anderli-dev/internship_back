# FastAPI Application

This is a FastAPI-based application.

## Prerequisites

Make sure you have the following installed:
- Python 3.9+
- pip

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

### Using Uvicorn

Start the application locally with Uvicorn:
```bash
uvicorn app.main:app --reload
```

The application doc will be available at:
- OpenAPI documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Using Docker

Build the Docker image:
```bash
docker build -t meduzzen-back-app -f app/Dockerfile .
```
Run the container:
```bash
docker run -d --name meduzzen-back-app -p 8000:8000 meduzzen-back-app
```

## Running Tests

Run the test suite using `pytest`:
```bash
pytest
```

To check code coverage:
```bash
pytest --cov=app
```
