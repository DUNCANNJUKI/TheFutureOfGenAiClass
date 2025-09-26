# WasteTracker (Jaseci Version)

A simple waste reporting system built using [Jac language](https://docs.jaseci.org/docs/jac/intro) and [Jaseci Framework](https://jaseci.org).

## Features

- 📥 Report waste items with **geo-location**.
- � Track which **user** reported each item.
- �📋 View a detailed list of all reported waste.
- 🕒 Timestamps are returned in a **human-readable format**.
- ⚡ Built on a flexible, graph-based backend.
- 🌐 Instantly available as a REST API via `jsserv`.

## Requirements

- Python 3.8+
- `pip install jaseci jaseci_serv`

## How to Run

### Method 1: Command-Line Interface (CLI)

1.  **Start the Jaseci Shell:**
    ```bash
    jsctl
    ```
2.  **Load the Jac program:**
    ```
    actions load module waste_tracker.jac
    ```
3.  **Run walkers:**

    **Report a new waste item:**
    ```
    walker run report_waste -ctx '{"user_name": "Duncan", "item_name": "Plastic Bottle", "lat": -1.286389, "lon": 36.817223}'
    ```

    **List all reported waste items:**
    ```
    walker run list_waste_reports
    ```

### Method 2: API Server

1.  **Start the Jaseci Server:**
    ```bash
    jsserv
    ```
2.  **Send POST requests to the API:**

    You can now use an API client (like `curl` or Postman) to interact with your walkers.

    **Report a new waste item:**
    *   **URL:** `http://127.0.0.1:8000/js/walker_run`
    *   **Method:** `POST`
    *   **Body:**
        ```json
        {
          "name": "report_waste",
          "ctx": {
            "user_name": "Alice",
            "item_name": "Cardboard Box",
            "lat": -1.2921,
            "lon": 36.8219
          }
        }
        ```

    **List all reported waste items:**
    *   **URL:** `http://127.0.0.1:8000/js/walker_run`
    *   **Method:** `POST`
    *   **Body:**
        ```json
        {
          "name": "list_waste_reports",
          "ctx": {}
        }
        ```

