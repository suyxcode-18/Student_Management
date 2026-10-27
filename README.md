# Student Management System

A full-stack Student Management System built with **FastAPI**,
**PostgreSQL**, **SQLAlchemy**, **Pydantic**, and a simple
**HTML/CSS/JavaScript** frontend. The project demonstrates REST API CRUD
operations and API testing with **Postman**, including Collection Runner
workflows.

## Table of Contents

-   [Features](#features)
-   [Technology Stack](#technology-stack)
-   [Project Structure](#project-structure)
-   [Prerequisites](#prerequisites)
-   [Installation and Setup](#installation-and-setup)
-   [Environment Configuration](#environment-configuration)
-   [Run the Application](#run-the-application)
-   [API Reference](#api-reference)
-   [Postman API Testing](#postman-api-testing)
-   [Collection Runner Workflow](#collection-runner-workflow)
-   [Troubleshooting](#troubleshooting)
-   [Security Notes](#security-notes)
-   [Future Improvements](#future-improvements)

## Features

### Backend

-   Create, read, update, and delete student records (CRUD).
-   PostgreSQL database integration using SQLAlchemy.
-   Pydantic request validation.
-   Duplicate email handling.
-   HTTP error responses for invalid or missing records.
-   Automatic interactive API documentation through Swagger UI.
-   Pagination parameters for listing students (`skip` and `limit`).

### Frontend

-   View student records in a table.
-   Add new students.
-   Edit existing student records.
-   Delete student records with a confirmation prompt.
-   Search by name, email, or course.
-   Summary cards for total students, average age, and number of
    distinct courses.
-   Success and error messages.

### API Testing

-   Test endpoints with Postman.
-   Verify response status codes and JSON response bodies.
-   Save requests in a Postman collection.
-   Use collection variables and a dynamically generated test email.
-   Run create, read, update, and delete requests in sequence using
    Collection Runner.

## Technology Stack

-   **Language:** Python
-   **Backend framework:** FastAPI
-   **Database:** PostgreSQL
-   **ORM:** SQLAlchemy
-   **Validation:** Pydantic
-   **Database driver:** Psycopg 3
-   **Frontend:** HTML, CSS, JavaScript
-   **API testing:** Postman
-   **ASGI server:** Uvicorn

## Project Structure

``` text
student_management/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, routes, CORS configuration
│   ├── database.py      # PostgreSQL engine and session dependency
│   ├── models.py        # SQLAlchemy Student model
│   ├── schemas.py       # Pydantic request/response schemas
│   └── crud.py          # Database CRUD functions
├── frontend/
│   └── index.html       # HTML/CSS/JavaScript UI
├── .env                 # Local database URL (do not commit)
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

Install or prepare the following:

1.  Python 3.10 or newer.
2.  PostgreSQL installed and running.
3.  A PostgreSQL database user and password.
4.  Postman (for API testing).
5.  A modern web browser.

## Installation and Setup

### 1. Clone or open the project

If the project is hosted in a Git repository:

``` bash
git clone <your-repository-url>
cd student_management
```

Otherwise, open the existing `student_management` folder in VS Code.

### 2. Create and activate a virtual environment

Windows PowerShell:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

``` bat
venv\Scripts\activate.bat
```

macOS/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

Create or check `requirements.txt`:

``` text
fastapi
uvicorn[standard]
sqlalchemy
psycopg[binary]
pydantic-settings
email-validator
```

Install packages:

``` bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

In pgAdmin's Query Tool or `psql`, run:

``` sql
CREATE DATABASE student_db;
```

Create the database only once. If it already exists, skip this command.

### 5. Configure the environment

Create `.env` in the project root:

``` env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/student_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password. If your password
contains special URL characters, URL-encode them in the connection URL.

Do not put real credentials in source code or commit `.env` to Git.

### 6. Check CORS configuration

If the frontend is served at `http://127.0.0.1:5500`, the FastAPI app
should allow that origin. In `app/main.py`, after creating the `FastAPI`
application, configure CORS as needed:

``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If you serve the frontend from a different origin, add that exact origin
to `allow_origins`.

## Run the Application

Open two terminals from the project root.

### Terminal 1: Start FastAPI

``` bash
uvicorn app.main:app --reload
```

Default local addresses:

-   API base URL: `http://127.0.0.1:8000`
-   Swagger UI: `http://127.0.0.1:8000/docs`
-   ReDoc: `http://127.0.0.1:8000/redoc`

Keep this terminal running.

### Terminal 2: Start the frontend

``` bash
python -m http.server 5500 --directory frontend
```

Open the UI in a browser:

-   Frontend: `http://127.0.0.1:5500`

The frontend calls the FastAPI backend. PostgreSQL is accessed by the
backend, not directly by the browser.

## API Reference

The routes below match the sample backend implementation in this
project.

Base URL:

``` text
http://127.0.0.1:8000
```

  --------------------------------------------------------------------------------
  Method            Endpoint                   Purpose           Typical success
                                                                 response
  ----------------- -------------------------- ----------------- -----------------
  GET               `/`                        Check that the    `200 OK`
                                               API is running    

  POST              `/students`                Create a student  `201 Created`

  GET               `/students`                List students     `200 OK`

  GET               `/students/{student_id}`   Get one student   `200 OK`

  PUT               `/students/{student_id}`   Replace/update    `200 OK`
                                               student fields    

  DELETE            `/students/{student_id}`   Delete a student  `200 OK`
  --------------------------------------------------------------------------------

The list endpoint supports pagination:

``` text
GET /students?skip=0&limit=100
```

The `limit` parameter must be between 1 and 100 in the sample
implementation.

### Student JSON format

Use this request body for `POST /students` and
`PUT /students/{student_id}`:

``` json
{
  "name": "Uday Singh",
  "age": 22,
  "email": "uday.singh@example.com",
  "course": "B.Tech CSE"
}
```

Notes: - The request requires `name`, `age`, `email`, and `course`. -
`age` must be an integer between 1 and 120. - `email` must be a valid
email address. - Email addresses must be unique in the database. - The
server generates the student `id`; do not send it in the create request.

### Common status codes

  Status                        Meaning
  ----------------------------- -------------------------------------------------
  `200 OK`                      Request succeeded
  `201 Created`                 Student created
  `404 Not Found`               Student ID or route was not found
  `409 Conflict`                Duplicate email or database constraint conflict
  `422 Unprocessable Entity`    Request validation failed
  `500 Internal Server Error`   Unexpected backend error

Exact response bodies can vary depending on the implementation and error
handler.

## Postman API Testing

### 1. Create a collection

1.  Open Postman.
2.  Create a collection named **Student Management API**.
3.  Add a collection variable:
    -   Variable: `base_url`
    -   Initial/current value: `http://127.0.0.1:8000`
4.  Save the collection.

Use `{{base_url}}` in request URLs.

### 2. Create and save these requests

  Request name        Method   URL
  ------------------- -------- ---------------------------
  Get All Students    GET      `{{base_url}}/students`
  Get Student By ID   GET      `{{base_url}}/students/1`
  Create Student      POST     `{{base_url}}/students`
  Update Student      PUT      `{{base_url}}/students/1`
  Delete Student      DELETE   `{{base_url}}/students/1`

For POST and PUT, select **Body → raw → JSON** and use a valid student
JSON object. For DELETE, use a test record you are comfortable removing.

### 3. Check response tests

For a GET request that returns a list, open **Scripts → Post-response**
and add:

``` javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is a JSON array", function () {
    pm.response.to.be.json;
    pm.expect(pm.response.json()).to.be.an("array");
});
```

This verifies the response status and list format. If you expect exactly
10 records, add a length assertion only when the database is expected to
contain exactly 10 students.

## Collection Runner Workflow

Use a dedicated test student so the workflow does not modify your
existing records.

### 1. Add these requests in this order

1.  `Create Test Student` --- POST `{{base_url}}/students`
2.  `Get Test Student` --- GET `{{base_url}}/students/{{student_id}}`
3.  `Update Test Student` --- PUT `{{base_url}}/students/{{student_id}}`
4.  `Delete Test Student` --- DELETE
    `{{base_url}}/students/{{student_id}}`
5.  `Verify Deleted Student` --- GET
    `{{base_url}}/students/{{student_id}}`

### 2. Create Test Student body

In **Body → raw → JSON**:

``` json
{
  "name": "Runner Test Student",
  "age": 22,
  "email": "{{test_email}}",
  "course": "B.Tech CSE"
}
```

In **Scripts → Pre-request** for this POST request:

``` javascript
pm.variables.set(
  "test_email",
  `runner.${Date.now()}@example.com`
);
```

In **Scripts → Post-response** for this POST request:

``` javascript
pm.test("Student created", function () {
  pm.response.to.have.status(201);
});

const data = pm.response.json();

pm.test("Response contains student ID", function () {
  pm.expect(data.id).to.exist;
});

pm.collectionVariables.set("student_id", data.id);
```

### 3. Test the GET request

For `Get Test Student`, use this Post-response script:

``` javascript
pm.test("Student can be retrieved", function () {
  pm.response.to.have.status(200);
});

const data = pm.response.json();

pm.test("Correct test student returned", function () {
  pm.expect(data.name).to.eql("Runner Test Student");
  pm.expect(data.id).to.eql(
    Number(pm.collectionVariables.get("student_id"))
  );
});
```

### 4. Test the PUT request

Use this body:

``` json
{
  "name": "Runner Updated Student",
  "age": 23,
  "email": "{{test_email}}",
  "course": "Data Analytics"
}
```

Post-response script:

``` javascript
pm.test("Student updated", function () {
  pm.response.to.have.status(200);
});

const data = pm.response.json();

pm.test("Updated fields are returned", function () {
  pm.expect(data.name).to.eql("Runner Updated Student");
  pm.expect(data.age).to.eql(23);
  pm.expect(data.course).to.eql("Data Analytics");
});
```

### 5. Test the DELETE request

Post-response script for `Delete Test Student`:

``` javascript
pm.test("Student deleted", function () {
  pm.response.to.have.status(200);
});

pm.test("Deletion confirmation returned", function () {
  pm.expect(pm.response.json().message)
    .to.eql("Student deleted successfully");
});
```

### 6. Verify deletion

For `Verify Deleted Student`, add:

``` javascript
pm.test("Deleted student returns 404", function () {
  pm.response.to.have.status(404);
});
```

### 7. Run the collection

1.  Save all requests and scripts.
2.  Select the collection and click **Run** / **Run collection**.
3.  Select all five requests in the correct order.
4.  Set **Iterations** to `1`.
5.  Click **Run Student Management API** (the button label can vary).

Expected results for the sample backend: POST `201`, GET `200`, PUT
`200`, DELETE `200`, and the final GET `404`. These are expected
outcomes, not a guarantee; your actual API responses determine the test
results.

## Troubleshooting

### PostgreSQL connection refused

-   Confirm the PostgreSQL service is running.
-   Verify the host and port in `.env` (commonly `localhost:5432`).
-   Confirm that the database exists.

### Password authentication failed

-   Verify the PostgreSQL username and password.
-   Check URL encoding for special characters in the password.

### `ModuleNotFoundError: No module named 'app'`

-   Run Uvicorn from the project root, the directory containing the
    `app` folder.

### `422 Unprocessable Entity`

-   Ensure the request body is valid JSON.
-   Check required field names and types.
-   Ensure `age` is an integer and `email` is valid.

### `409 Conflict`

-   The email may already exist. Use a different email for a new
    student.

### CORS error in the browser

-   Check that the frontend origin exactly matches an entry in
    `allow_origins`.
-   Use the frontend HTTP server rather than opening `index.html`
    directly as a `file://` URL.

### `Connection refused` in Postman

-   Start Uvicorn.
-   Verify that the URL uses the correct host and port.

### Collection Runner tests fail

-   Confirm the POST request succeeded before running GET, PUT, and
    DELETE.
-   Ensure `student_id` is saved as a collection variable.
-   Verify request order and JSON bodies.
-   Inspect the failed response body and the FastAPI terminal logs.

## Security Notes

-   Never commit `.env`, passwords, or production credentials.
-   Use test records for automated tests, particularly for DELETE
    requests.
-   The frontend and API configuration here are intended for local
    development.
-   Restrict CORS origins in production.
-   Use database migrations, authentication, authorization, and
    appropriate deployment settings before production use.
-   The sample API does not include user authentication.

## Future Improvements

-   Add partial updates with `PATCH`.
-   Add authentication and role-based authorization.
-   Add Alembic migrations.
-   Add automated backend tests with `pytest` and FastAPI's test client.
-   Add sorting, filtering, and server-side pagination.
-   Deploy the backend, frontend, and database using production-ready
    hosting.

------------------------------------------------------------------------

**Author:** Add your name here\
**Project:** Student Management System\
**Purpose:** Learning FastAPI, PostgreSQL, frontend integration, REST
APIs, and Postman testing.
