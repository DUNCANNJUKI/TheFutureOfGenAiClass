# Waste Tracker API

This is a simple FastAPI-based API for tracking waste. It allows you to create, retrieve, and delete waste records.

## Project Structure

The project is structured as follows:

- `app/`: Main application folder
  - `main.py`: FastAPI application entry point
  - `database.py`: Database connection and session management
  - `models/`: SQLAlchemy models
    - `waste.py`: `Waste` model
  - `routes/`: API routes
    - `waste.py`: Waste management routes
- `requirements.txt`: Project dependencies

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `POST /waste/`: Create a new waste record
- `GET /waste/`: Get all waste records
- `GET /waste/{waste_id}`: Get a specific waste record by ID
- `DELETE /waste/{waste_id}`: Delete a specific waste record by ID
"
"
"
