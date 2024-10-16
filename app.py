from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nigeriawillbegreat'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
db = SQLAlchemy(app)

# Define User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Define Quiz Model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)

# Define Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(150), nullable=False)

# Define Answer Choice Model
class AnswerChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(150), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)