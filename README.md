To run this project, do the following steps:
1. Make your python environment<br>`python -m venv venv`
2. Install requirements<br>`pip install -r requirements.txt`
3. Create your google cloud service account and download the credentials.json file and place it in the root folder.
4. Create your database and setup the database url in the .env file
5. To create the tables in the database, go to the root folder and run<br> `python setup_db.py`
6. Run flask app<br>`python run.py`



# Routes File

This file contains API endpoints for managing users, forms, questions, responses, and answers in a Flask application.

## User APIs

- `/create_user`: Endpoint to create a new user. Only accepts 'admin' or 'customer' user types.
- `/delete_user/<uuid:user_id>`: Endpoint to delete a user by user ID.
- `/get_all_users`: Endpoint to retrieve all users.

## Form APIs

- `/create_form`: Endpoint to create a form. Accessible only to 'admin' users.

## Question APIs

- `/create_question`: Endpoint to create a question associated with a specific form ID.

## Response APIs

- `/create_response`: Endpoint to create a response for a form by a 'customer' user.
- `/submit_response`: Endpoint to submit a response for a form.

## Answer APIs

- `/create_answer`: Endpoint to create an answer for a specific question in a response.

### Important Notes:

- This routes file handles the creation, deletion, and retrieval of users, forms, questions, responses, and answers.
- The file utilizes Flask and gspread to interact with Google Sheets.
- Credentials for Google Sheets authentication are stored in 'credentials.json'. Ensure this file exists and contains the necessary credentials.
