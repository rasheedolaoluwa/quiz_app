# Interactive Quiz Application

An engaging, web-based interactive quiz platform where users can register, create quizzes, take quizzes, and compete for high scores on the leaderboard. The application provides a fun and educational experience, allowing users to track their progress and challenge themselves.

## Author
Rasheed Olaoluwa ([Email](radeyola@gmail.com), [Twitter](https://x.com/Rasheed0laoluwa), [Github](https://github.com/rasheedolaoluwa)).

## Table of Contents
- [About](#about)
- [Features](#features)
- [Architecture & Technologies Used](#architecture--technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## About

The **Interactive Quiz Application** is a web-based platform designed to allow users to:
- Create their own quizzes.
- Take quizzes with timers to enhance engagement.
- Track their quiz attempts and scores.
- Compete with others through a leaderboard.

This app is perfect for users who want to practice their knowledge and compete against friends or other users for the highest scores.

## Features

- **User Registration and Login**: Secure user authentication with password hashing.
- **Quiz Creation**: Users can create quizzes with multiple-choice questions.
- **Take Quizzes**: Timed quizzes that users can take and immediately see their scores.
- **Results History**: Users can view their past quiz attempts and scores.
- **Leaderboard**: Displays the top scores for each quiz.

## Architecture & Technologies Used

- **Backend**: Flask (Python) - RESTful backend that manages quiz data, user sessions, and interactions.
- **Frontend**: HTML, CSS, JavaScript, Bootstrap - For building responsive user interfaces.
- **Database**: SQLite - For storing user data, quizzes, and results during development.
- **Deployment**: [Railway](https://railway.app) - For deploying and hosting the web application.
- **Other Technologies**:
  - **Gunicorn**: WSGI server used for deployment.
  - **Flask-WTF**: For form handling and input validation.
  - **Flask-Login**: Manages user authentication and sessions.

## Installation

To run this project locally, follow these steps:

### Prerequisites
- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/) (Python package manager)
- [Git](https://git-scm.com/)

### Steps

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/rasheedolaoluwa/quiz_app.git
   cd quiz_app
2. **Create a Virtual Environment**:
   ```sh
   python -m venv env
3. **Activate the Virtual Environment**:
   ```sh
   On Windows:
   .\env\Scripts\activate
   On macOS/Linux:
   source env/bin/activate 
4. **Install Dependencies:**:
   ```sh
   pip install -r requirements.txt
5. **Set Environment Variables**:
   - Create a .env file or set the environment variables in your system.
   - Set the SECRET_KEY:
   ```sh
   SECRET_KEY='your_secret_key_here'
6. **Run the Application**:
   ```sh
   python app.py
7. **Run the Application**:
   - Open your browser and navigate to http://127.0.0.1:5000.
  
## Usage
- **User Registration**: Create an account and log in.
- **Create a Quiz**: Navigate to the home page and select the option to create a new quiz.
- **Take Quizzes**: Select a quiz from the list and try to get the highest score.
- **View Leaderboard**: Check the leaderboard to see the top scorers for each quiz.
- **Track Results**: View your previous quiz attempts under "My Quiz Results."

## Deployment
This application has been deployed using Railway. If you would like to deploy this project on Railway, follow these steps:
- **Create a Railway Account**: Sign up at [Railway](https://railway.app).
- **Connect GitHub Repo**: Link your GitHub repository to a new Railway project.
- **Add Environment Variables**: Add your SECRET_KEY to the project's environment settings.
- **DNS Configuration**: Add a custom domain via the Railway settings if desired.

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature/your-feature).
- Make your changes.
- Commit your changes (git commit -m 'Add a new feature').
- Push to the branch (git push origin feature/your-feature).
- Open a pull request.

## Feature Ideas
- Adding True/False questions.
- Integrating an external API to get new quiz questions.
- Improving user experience with enhanced UI elements or animations.

## License
This project is open-source and available under the MIT License. You are free to use, modify, and distribute this software as long as the original copyright notice and permissions appear in all copies.
