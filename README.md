# CITS5505 Agile Web Dev Group Project: Online Formative Assessment
Authors: Veronica Rao (23030918) and Aaron Norrish (21972015)

## Running the application
### Installation and Set-Up
First navigate to the root directory and create a virtual environment:
```
python3 -m venv ./venv
```

then activate the environment and install the required packages:
```
source ./venv/bin/activate
pip install -r "requirements.txt"
```

download and install [SQLite](http://sqlite.org/download.html)

build and migrate the database:
```
flask db init
flask db upgrade
```

to populate the database with quizzes (this must be done):
```
python3 setup_db.py
```

optionally, if you want to populate the database with some sample users and their answers:
```
python3 add_dummies.py
```

### Running the application
finally run the application:
```
python3 main.py
```

the app should now be up and running on local host, port 5000: http://localhost:5000/

## Purpose, Context and Assessment Mechanism
This web application aims to assist users in developing their Italian language skills. 
In doing so, this web application provides information pages, where a user can memorise definitions and read information about any chosen topic. To enhance this memorisation process, assessments are added for each topic, to allow a user to test out what they have learnt.
The assessment consists a variety of means. This includes multiple choice questions, multiple selection questions and inserting the correct answer type of questions.
After completing an assessment, a user is able to see what questions they have gotten correct and incorrect, and the correct solution is also given.

## Unit Tests
The unit tests for this web application tests functions created with the application. 
This includes retrieving questions, solutions, user answers next model. These tests check if the application correctly identifies and populates these variables.

Other unit tests include functions to check a user logging in and signing up to the web application. For the signing up method, it is broken down to testing when there is a missing field, a unique user and a successful sign up. Similar to the signing up method, the log-in method checks for a successful sign up.

*Please note that LiveServer was not implemented for these tests*

To run the unit testing for this web application, please make sure the aforementioned steps are completed.

For selenium tests, make sure the Google web driver is installed and that it is installed in the test directory.
Within the terminal 
```
flask run
```

In a new terminal window, change to the working directory and make sure the vitrual environment is activated (please look above if unsure)

### Running tests
```
python3 tests.py
```

## Architecture and Design
Initial design for the front-end can be seen in TODO

The application architecture is based on the Model-View-Control design pattern. Our application consists of three main models: 
* User — stores a name, email address (must be unique), and a password hash. Users are distinguished by a unique id. This model has methods to set and check a user password, get the user's progress (percentage of quizzes completed), and to get the next module the user should complete.
* Quiz — stores a name, questions (each question has three attributes associated with it — the text, the type of question (determines the required form input field), and possible answer choices (this field is null if the question is not multi-choice)), and solutions to the questions. Each quiz must have at least 4 questions, and can have at most 8 questions. This class has methods for retrieving the questions and answers (separately) for a given quiz. 
* UserAnswer — stores a user answer for a given quiz. As such, each entry in the table it distinguished by the corresponding quiz id and the user id. The user's score for that quiz is also stored (as a decimal between 0 and 1.) This class has a method for retrieving a user's answers.

The application control logic is handled in controllers.py; routing functions simply call a function in controllers.py.

It should be noted that we did that we do not think think this design is perfect. This way of storing quizzes has a lot of redundancies: obviously, the fact that each solution is stored as a 20 character string when in some cases the solution only requires a single character is not ideal. Nor the fact that we have a "choices" attribute for each question even though some questions do not actually have choices associated with them, or that a quiz size is limited to 8 questions (the majority of our quizzes only have 4 questions so most of this table is null.) Perhaps a non-relational database would be better suited. 

Initially, we were storing the text and choices for a given quiz in a flask form object and only storing the user answers in the database (e.g. we had an AlphabetQuiz form and a corresponding AlphabetQAnswers table, and so on for each type of quiz.) This way, we did not have the redundancy of our current approach, but it had the flaw that if someone wanted to add more quizzes they would have to manually create a new flask form object and corresponding answers table in the database. We realised this lack of extensibility was not ideal and we needed to completely refactor this part of our application. In our new approach, we generate a flask form object (representing a given quiz) on the fly, so adding a new quiz is as simple as adding a new entry to the database.

In the development process, we utilised a Kanban board (can be seen on the GitHub) to organise and display which tasks needed to be done. Yet to be completed tasks were divided into "Must Haves" and "Nice to Haves".

## Git Log
The git log can be found in git-log.txt. Note that the author "ge75ceb" is also Aaron Norrish.

## References
A number of external libraries were used in this project:

* Python Libraries:
    * flask
    * flask-wtf
    * flask-sqlalchemy
    * flask-migrate
    * flask-login
    * python-dotenv
    * email-validator
    * selenium

* SQLite

* Bootstrap v4.6
    * log-in and sign-up page CSS has been adapted from "Bootstrap Examples", as has the dashboard template

* jQuery

* Icons have been taken from Bootstrap, [FontAwesome](https://fontawesome.com/) and www.flaticon.com
    * Italian flag icon made by Freepik from www.flaticon.com

* Charts from Chart.js