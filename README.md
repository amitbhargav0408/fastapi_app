# FastAPI CRUD Application

This project is a FastAPI application that implements CRUD operations for two entities: **Items** and **User Clock-In Records**. It uses MongoDB for data storage and supports various filtering options as well as aggregation queries.

## Features

- **Items API**:
  - Create, read, update, and delete items.
  - Filter items by email, expiry date, insert date, and quantity.
  - Aggregate items to return counts grouped by email.

- **Clock-In Records API**:
  - Create, read, update, and delete user clock-in records.
  - Filter clock-in records by email, location, and insert date.

## Technologies Used

- FastAPI
- MongoDB (via pymongo)
- Pydantic for data validation
- Uvicorn for running the app

## Getting Started

### Prerequisites

- Python 3.7 or higher
- MongoDB instance (local or MongoDB Atlas)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amitbhargav0408/fastapi_app.git
   cd fastapi_app
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   pip install -r requirements.txt
   ```

3. **Important:** **Configure your MongoDB connection in `app/database.py`.**
   
   > **⚠️ Important:**  
   > Before running the application, you **must** update the `mongodb_url` variable in `app/database.py` with your actual MongoDB connection string. This ensures that the application connects to the correct database instance.
   >
   > Example:
   > ```python
   > # app/database.py
   > from pymongo import MongoClient
   > import os
   >
   > MONGODB_URL = os.getenv("MONGODB_URL", "your_actual_mongodb_connection_string")
   > client = MongoClient(MONGODB_URL)
   > db = client.your_database_name
   > ```

   **Recommendation:**  
   For better security and flexibility, consider using environment variables to store your MongoDB connection string instead of hardcoding it. You can use packages like `python-dotenv` to manage environment variables.

### Running the Application

Run the application with:
```bash
uvicorn app.main:app --reload
```

### API Documentation

The API documentation is available at `http://localhost:8000/docs` when the server is running.

## API Endpoints

### Items API

- **POST /items**
  - Create a new item.
  - **Request Body**:
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com",
      "item_name": "Apple",
      "quantity": 10,
      "expiry_date": "2024-12-31"
    }
    ```
  - **Response**:
    ```json
    {
      "id": "unique_item_id"
    }
    ```

- **GET /items/{id}**
  - Retrieve an item by ID.
  - **Response**:
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com",
      "item_name": "Apple",
      "quantity": 10,
      "expiry_date": "2024-12-31",
      "insert_date": "2023-10-01T12:00:00Z"
    }
    ```

- **GET /items/filter**
  - Filter items based on:
    - Email (exact match).
    - Expiry Date (filter items expiring after the provided date).
    - Insert Date (filter items inserted after the provided date).
    - Quantity (items with quantity greater than or equal to the provided number using a `gte` filter).
  - **Example Query**: `/items/filter?email=john@example.com&expiry_date=2023-01-01&insert_date=2023-01-01&quantity=5`

- **DELETE /items/{id}**
  - Delete an item based on its ID.
  - **Response**: No content.

- **PUT /items/{id}**
  - Update an item’s details by ID (excluding the Insert Date).
  - **Request Body**:
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com",
      "item_name": "Banana",
      "quantity": 5,
      "expiry_date": "2024-11-30"
    }
    ```

- **GET /items/aggregate**
  - Aggregate data to return the count of items for each email (grouped by email).
  - **Response**:
    ```json
    [
      {
        "email": "john@example.com",
        "count": 5
      },
      {
        "email": "jane@example.com",
        "count": 3
      }
    ]
    ```

### Clock-In Records API

- **POST /clock-in**
  - Create a new clock-in entry.
  - **Request Body**:
    ```json
    {
      "email": "john@example.com",
      "location": "Office"
    }
    ```
  - **Response**:
    ```json
    {
      "id": "unique_clock_in_id"
    }
    ```

- **GET /clock-in/{id}**
  - Retrieve a clock-in record by ID.
  - **Response**:
    ```json
    {
      "email": "john@example.com",
      "location": "Office",
      "insert_datetime": "2023-10-01T08:00:00Z"
    }
    ```

- **GET /clock-in/filter**
  - Filter clock-in records based on:
    - Email (exact match).
    - Location (exact match).
    - Insert DateTime (clock-ins after the provided date).
  - **Example Query**: `/clock-in/filter?email=john@example.com&location=Office&insert_datetime=2023-01-01`

- **DELETE /clock-in/{id}**
  - Delete a clock-in record based on its ID.
  - **Response**: No content.

- **PUT /clock-in/{id}**
  - Update a clock-in record by ID (excluding Insert DateTime).
  - **Request Body**:
    ```json
    {
      "email": "john@example.com",
      "location": "Home"
    }
    ```

## Docker Integration

The application can be containerized and deployed using Docker.

### Building and Running the Docker Container

1. Build the Docker image:
   ```bash
   docker build -t amitbhargav/fastapiapp:latest .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 amitbhargav/fastapiapp:latest
   ```

### Pushing to Docker Hub

1. Tag the Docker image:
   ```bash
   docker tag amitbhargav/fastapiapp:latest amitbhargav/fastapiapp:tagname
   ```

2. Push the image to Docker Hub:
   ```bash
   docker push amitbhargav/fastapiapp:tagname
   ```

### Pulling from Docker Hub

To use the Docker image on another machine or server, pull it from Docker Hub:

```bash
docker pull amitbhargav/fastapiapp:latest
```

## Deployment

The application is hosted on [Koyeb](https://glad-merralee-wacky12-a801f7ca.koyeb.app), and the [Swagger UI](https://app.swaggerhub.com/apis/AmitBhargav/items-and_clock_in_records_api/1.0.0) is accessible for testing the APIs.

## Contributing

Feel free to fork the repository, make changes, and create a pull request!

## License

This project is licensed under the MIT License.
