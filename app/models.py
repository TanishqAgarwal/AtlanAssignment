from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid
from app.app import db

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.String)
    form_id = db.Column(UUID(as_uuid=True), db.ForeignKey('form.id'))
    required = db.Column(db.Boolean)

class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    form_name = db.Column(db.String)
    # action = db.Column(db.Enum('example_action_1', 'example_action_2'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = db.Column(UUID(as_uuid=True), db.ForeignKey('question.id'))
    response_id = db.Column(UUID(as_uuid=True), db.ForeignKey('response.id'))
    text = db.Column(db.String)

class Response(db.Model):
    __tablename__ = 'response'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_id = db.Column(UUID(as_uuid=True), db.ForeignKey('form.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

class SubmittedResponse(db.Model):
    __tablename__ = 'submittedresponse'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_id = db.Column(UUID(as_uuid=True), db.ForeignKey('form.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_type = db.Column(db.Enum('admin', 'customer', name='app_user'))
