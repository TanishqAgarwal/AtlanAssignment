from app.app import create_app, db
from app.models import Question, Form, Answer, Response, User

# Create the Flask app
app = create_app()

# Access the app's database instances

# Create the database tables
with app.app_context():
    db.create_all()