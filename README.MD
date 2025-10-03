This repository demonstrates how a simple Flask frontend can interact with a Flask backend/API. It also includes Docker and Docker Compose setups, with and without a PostgreSQL database, to show different deployment scenarios.

```
Frontend (Flask, port 5000)  --->  Backend API (Flask, port 8080)  --->  PostgreSQL DB (port 5432, optional)
```

# Routes
## Backend / API
- `/data`: Returns a sample item, with id, name and description.
- `/random`: Returns a random number and generated string
- `/status`: Returns a simple status message
- `/users`: Get all users (GET) or create a new user (POST)
- `/users/<id>`: Delete a user by ID (DELETE) or update a user by ID (PUT)

## Frontend
- `/`: Home page, displays the data from each API route with a reload button.
- `/users`: Displays all users and a form to create a new user. With options to delete or update each user.

# Running the example
There are two possible ways to run the example, either with Docker or manually with Python.

Both methods require you to have the backend and frontend servers running at the same time.

Clone the repository with the following command and navigate to the `api-example` folder in your terminal.
```bash
git clone https://github.com/Zeptiny/api-example.git
cd api-example
```

## Manually
1. Make sure you have Python installed.
2. Navigate to the `basic` folder in your terminal.
3. Create a virtual environment with `python -m venv venv` and activate it
   - Windows: `venv\Scripts\activate`
   - Linux / MacOS: `source venv/bin/activate`
4. Navigate to the `backend` folder
5. Install the required packages with `pip install -r requirements.txt`
6. Run the backend server with `flask run --port 8080`
7. Open a new terminal window and navigate to the `frontend` folder
8. Activate the virtual environment you created in step 3
9. Install the required packages with `pip install -r requirements.txt`
10. Run the frontend server with `flask run`
11. Open your browser and go to `http://localhost:5000`
12. You should see the frontend page displaying data from the backend API.

## Docker
1. Make sure you have Docker installed and running.
2. Navigate to the `docker` folder in your terminal.
3. Build and run the Docker images with `docker compose up`.
4. Open your browser and go to `http://localhost:5000`.
5. You should see the frontend page displaying data from the backend API.

## Docker With Database
This example uses a PostgreSQL database to store user data in a persistent manner.
When the backend starts, it automatically checks and creates the `users` table if it does not exist.

You can configure the database connection using the following environment variables:
- `DB_HOST`: The hostname of the database server (default: `db`)
- `DB_PORT`: The port of the database server (default: `5432`)
- `DB_NAME`: The name of the database (default: `backend_db`)
- `DB_USER`: The username to connect to the database (default: `admin`)
- `DB_PASSWORD`: The password to connect to the database (default: `admin`)

1. Make sure you have Docker installed and running.
2. Navigate to the `docker-with-db` folder in your terminal.
3. Build and run the Docker images with `docker compose up`.
4. Open your browser and go to `http://localhost:5000`.
5. You should see the frontend page displaying data from the backend API.
