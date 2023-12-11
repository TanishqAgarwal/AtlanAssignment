
import gspread
import uuid
from flask import Blueprint, jsonify, request
from app.app import db
from app.models import User, Form, Question, Response, Answer, SubmittedResponse

bp = Blueprint('routes', __name__)



####################################################################
# User apis
# API Endpoint to create a user
@bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_type = data.get('user_type')

    if user_type not in ['admin', 'customer']:
        return jsonify({'message': 'Invalid user type'}), 400

    new_user = User(user_type=user_type)
    db.session.add(new_user)
    db.session.commit()
    
    client = gspread.service_account(filename='credentials.json')
    wb_1 = client.open('Atlan Backend Assignment')
    wb_1_names = wb_1.get_worksheet(0)

    print(wb_1_names)
    return jsonify({'message': 'User created successfully', 'user_id': str(new_user.id)}), 201

# API Endpoint to delete a user
@bp.route('/delete_user/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

# API Endpoint to get all users
@bp.route('/get_all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [{'id': str(user.id), 'user_type': user.user_type} for user in users]

    return jsonify({'users': user_list}), 200



####################################################################
# Form APIs
# API Endpoint to create a form (accessible only to 'admin' users)
@bp.route('/create_form', methods=['POST'])
def create_form():
    data = request.get_json()
    user_id = data.get('user_id')
    form_name = data.get('form_name')
    # Check if the user exists and is an admin
    user = User.query.filter_by(id=user_id, user_type='admin').first()
    if not user:
        return jsonify({'message': 'User not found or not authorized to create forms'}), 401

    new_form = Form(
        owner=user_id,
        form_name=form_name)  # Assign the form to the user
    db.session.add(new_form)
    db.session.commit()

    client = gspread.service_account(filename='credentials.json')
    wb_1 = client.open('Atlan Backend Assignment')

    new_sheet_title = str(form_name)
    new_sheet = wb_1.add_worksheet(title=new_sheet_title, rows="100", cols="20")

    return jsonify({'message': 'Form created successfully', 'form_id': str(new_form.id), 'form_name':form_name}), 201


####################################################################
# Question APIs
# API endpoint to create a question
@bp.route('/create_question', methods=['POST'])
def create_question():
    data = request.get_json()
    user_id = data.get('user_id')
    form_id = data.get('form_id')
    text = data.get('text')
    required = data.get('required')

    # Check if the user exists and is an admin or has the necessary privileges
    user = User.query.filter_by(id=user_id, user_type='admin').first()
    if not user:
        return jsonify({'message': 'User not authorized or does not exist'}), 401

    # Check if the form_id exists or create a new check according to your logic
    form = Form.query.get(form_id)
    if not form:
        return jsonify({'message': 'Form not found'}), 404

    # Create a new question
    new_question = Question(
        text=text,
        form_id=form_id,
        required=required
    )
    db.session.add(new_question)
    db.session.commit()

    # Authenticate with Google Sheets using service account credentials
    client = gspread.service_account(filename='credentials.json')

    # Open the workbook
    wb_1 = client.open('Atlan Backend Assignment')

    # Get the form name associated with the form_id
    form_name = form.form_name

    # Find the corresponding sheet in the workbook
    sheet = wb_1.worksheet(form_name)

    # Find the last filled cell in the last column of the first row
    values_list = sheet.row_values(1)  # Retrieve the first row values
    last_filled_cell = len(values_list) + 1  # To find the next empty cell in the first row

    # Add the question text to the sheet in the next empty cell in the first row
    sheet.update_cell(1, last_filled_cell, text)

    return jsonify({'message': 'Question created successfully', 'question_id': str(new_question.id)}), 201


####################################################################
# API Endpoint to create a response
@bp.route('/create_response', methods=['POST'])
def create_response():
    data = request.get_json()
    form_id = data.get('form_id')
    user_id = data.get('user_id')

    # Check if the user is of type 'customer'
    user = User.query.filter_by(id=user_id, user_type='customer').first()
    if not user:
        return jsonify({'message': 'User is not a customer'}), 400

    new_response = Response(form_id=form_id, user_id=user_id)
    db.session.add(new_response)
    db.session.commit()

    return jsonify({'message': 'Response created successfully', 'response_id': str(new_response.id)}), 201


####################################################################
# API Endpoint to create an answer
@bp.route('/create_answer', methods=['POST'])
def create_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    response_id = data.get('response_id')
    text = data.get('text')

    if not (question_id and response_id and text):
        return jsonify({'message': 'Incomplete data provided'}), 400
    
    # Check if the question exists
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'message': 'Question does not exist'}), 404

    # Get the form_id associated with the question
    form_id = question.form_id

    # Retrieve the form_name from the form_id
    form = Form.query.get(form_id)
    if not form:
        return jsonify({'message': 'Form not found'}), 404
    
    form_name = form.form_name

    
    new_answer = Answer(question_id=question_id, response_id=response_id, text=text)
    db.session.add(new_answer)
    db.session.commit()

    return jsonify({'message': 'Answer created successfully', 'answer_id': str(new_answer.id)}), 201




# API Endpoint to submit a response
@bp.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.get_json()
    response_id = data.get('response_id')

    # Retrieve the response using response_id
    response = Response.query.get(response_id)

    if not response:
        return jsonify({'message': 'Response not found'}), 404
    
    # Extract form_id and user_id from the response
    form_id = response.form_id
    user_id = response.user_id

    form = Form.query.get(form_id)
    if not form:
        return jsonify({'message': 'Form not found'}), 404

    form_name = form.form_name

    # Get all answers in that response
    answers = Answer.query.filter_by(response_id=response_id).all()

    # Create an array of question_id and text
    question_text_array = [{'question_id': answer.question_id, 'text': answer.text} for answer in answers]

    # Fetch Question Texts using Question IDs:
    question_texts = []
    for item in question_text_array:
        question = Question.query.get(item['question_id'])
        if question:
            question_texts.append({'question_text': question.text, 'answer_text': item['text']})

    
    # Authenticate with Google Sheets using service account credentials
    client = gspread.service_account(filename='credentials.json')

    # Open the workbook
    wb_1 = client.open('Atlan Backend Assignment')

    # Access the sheet corresponding to the form_name
    sheet = wb_1.worksheet(form_name)

    for item in question_texts:
        # Find the column index with the matching question text
        first_row_values = sheet.row_values(1)  # Get the values in the first row
        column_index = first_row_values.index(item['question_text']) + 1

        # Get all values in the column
        column_values = sheet.col_values(column_index)

        # Find the last filled cell in the column and add the answer text to the next row
        last_filled_cell = len(column_values) + 1
        sheet.update_cell(last_filled_cell, column_index, item['answer_text'])

    # Create a new entry in SubmittedResponse table
    new_submitted_response = SubmittedResponse(form_id=form_id, user_id=user_id)
    db.session.add(new_submitted_response)
    db.session.commit()

    return jsonify({'message': 'Response created successfully', 'submitted_response_id': str(new_submitted_response.id)}), 201
