Frontend and Backend / API communication examples, both made with Flask.
The frontend was made with flask to make use of environment variables and Jinja templating.

# Routes
## Backend / API
- `/data`: Returns a sample item, with id, name and description.
- `/random`: Returns a random number and generated string
- `/status`: Returns a simple status message
- `/users`: Get all users (GET) or create a new user (POST)
- `/users/<id>`: Get a user by ID (GET) or delete a user by ID (DELETE)

## Frontend
- `/`: Home page, displays the data from each API route with a reload button.

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
10. Run the frontend server with `BACKEND_URL=http://localhost:8080 flask run`
11. Open your browser and go to `http://localhost:5000`
12. You should see the frontend page displaying data from the backend API.

## Docker
1. Make sure you have Docker installed and running.
2. Navigate to the `docker` folder in your terminal.
3. Build and run the Docker images with `docker compose up`.
4. Open your browser and go to `http://localhost:5000`.
5. You should see the frontend page displaying data from the backend API.
