# Copilot Instructions

This document provides instructions for using GitHub Copilot with the WasteTracker API project.

## Project Overview

This is a simple RESTful API built with FastAPI to track waste data. It uses SQLAlchemy for the ORM and `aiosqlite` for async database operations with a SQLite database.

## Key Files and Directories

-   `app/main.py`: The main entry point for the FastAPI application. It initializes the app and includes the routers.
-   `app/database.py`: Sets up the database connection and session management. It uses an `async` context for database sessions.
-   `app/models/waste.py`: Defines the `Waste` SQLAlchemy model, which represents the `waste` table in the database.
-   `app/routes/waste.py`: Contains all the API endpoints related to waste management (`/waste`). It handles CRUD operations for waste records.
-   `requirements.txt`: Lists all the Python dependencies for the project.

## Development Workflow

1.  **Environment Setup**:
    -   It's recommended to use a virtual environment.
    -   Install dependencies with `pip install -r requirements.txt`.

2.  **Running the Application**:
    -   Use `uvicorn app.main:app --reload` to run the server in development mode. The `--reload` flag automatically restarts the server on code changes.
    -   The API will be available at `http://127.0.0.1:8000`.

3.  **Database**:
    -   The application uses a SQLite database file (`waste.db`).
    -   The database tables are automatically created based on the models in `app/models/` when the application starts.

## Architectural Patterns

-   **FastAPI Routers**: The API is organized using FastAPI's `APIRouter`. The waste-related endpoints are grouped in `app/routes/waste.py`.
-   **Dependency Injection**: FastAPI's dependency injection system is used to manage database sessions. The `get_db` function in `app/routes/waste.py` is a dependency that provides a database session to the route functions.
-   **Pydantic Models**: Pydantic models are used for data validation and serialization. `WasteCreate` is used for creating new waste records, and `WasteOut` is used for responses.

## How to Contribute

-   When adding new endpoints, follow the existing pattern in `app/routes/waste.py`.
-   If you add new models, create a new file in the `app/models/` directory and make sure they are imported so that SQLAlchemy can create the tables.
-   Ensure any new dependencies are added to `requirements.txt`.
