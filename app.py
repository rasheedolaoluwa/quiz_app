from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define Quiz Model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)

# Define Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(150), nullable=False)
    option_a = db.Column(db.String(150), nullable=False)
    option_b = db.Column(db.String(150), nullable=False)
    option_c = db.Column(db.String(150), nullable=False)
    option_d = db.Column(db.String(150), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

# Define Answer Choice Model
class AnswerChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(150), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

# Define a Registration Form class
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

# Define Quiz Result Class
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='results')
    quiz = db.relationship('Quiz', backref='results')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.password = form.password.data  # This will hash the password
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/my_results')
@login_required
def my_results():
    results = QuizResult.query.filter_by(user_id=current_user.id).join(Quiz).add_columns(
        Quiz.title, QuizResult.score, QuizResult.timestamp
    ).all()
    return render_template('my_results.html', results=results)

@app.route('/leaderboard/<int:quiz_id>')
def leaderboard(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    top_results = QuizResult.query.filter_by(quiz_id=quiz_id).join(User).add_columns(
        User.username, QuizResult.score, QuizResult.timestamp
    ).order_by(QuizResult.score.desc()).limit(10).all()
    return render_template('leaderboard.html', quiz=quiz, top_results=top_results)

@app.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        question_text = request.form['question_text']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_answer = request.form['correct_answer']

        # Create the question with all options provided
        new_question = Question(
            text=question_text,
            correct_answer=correct_answer,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            quiz_id=quiz.id
        )
        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_question.html', quiz=quiz)

@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        new_quiz = Quiz(title=title)
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz created successfully!')
        return redirect(url_for('home'))
    return render_template('create_quiz.html')

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    if request.method == 'POST':
        score = 0
        total_questions = len(questions)
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer and user_answer.strip().lower() == question.correct_answer.lower():
                score += 1

        # Save quiz result to the database
        result = QuizResult(user_id=current_user.id, quiz_id=quiz_id, score=score)
        db.session.add(result)
        db.session.commit()

        # Flash feedback to the user
        flash(f'You scored {score} out of {total_questions}', 'success')
        return redirect(url_for('home'))

    return render_template('take_quiz.html', quiz=quiz, questions=questions)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    quizzes = Quiz.query.all()
    return render_template('home.html', quizzes=quizzes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)