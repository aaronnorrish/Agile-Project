from learn_italian_flask import app
from learn_italian_flask import db
from flask import render_template, redirect, url_for, flash
from learn_italian_flask.forms import LoginForm, SignupForm, QuizForm, MultiCheckboxField
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User, Quiz, UserAnswer

# test
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectMultipleField, widgets
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length, NumberRange

def get_index():
    return render_template('index.html', title="La Bella Lingua")

def get_statistics():
    # determine the total number of quizzes completed by users
    all_user_quizzes = UserAnswer.query.all()
    num_quizzes_completed = sum([1 for quiz in all_user_quizzes])
    all_quizzes = Quiz.query.all()

    # get the quiz names
    labels = []
    if all_quizzes is not None:
        labels = [quiz.name for quiz in all_quizzes]

    # determine the average score across quizzes
    cumulative_scores = [0 for i in range(len(labels))]
    attempts = [0 for i in range(len(labels))]
    for quiz in all_user_quizzes:
        cumulative_scores[quiz.quiz_id-1] += quiz.score * 100
        attempts[quiz.quiz_id-1] += 1
    scores = [round(score/attempt) if attempt != 0 else 0 for score, attempt in zip(cumulative_scores, attempts)]

    # determine the number of users signed up to the website
    users = User.query.all()
    num_users = sum([1 for user in users])
    return render_template('statistics.html', title="La Bella Lingua — Usage Statistics", labels=labels, scores=scores, num_users=num_users, num_quizzes_completed=num_quizzes_completed)

def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    # if the user is a valid user redirect to the dashboard, otherwise stay on the login page
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('log-in.html', title="La Bella Lingua — Log in", form=form)

def user_signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        # if the user sign up details are valid (unique email address) add to the db and login
        # otherwise stay on page
        if User.query.filter_by(email=form.email.data).first() is not None:
            flash('This email is taken!')
            return redirect(url_for('signup'))
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('sign-up.html', title="La Bella Lingua — Sign up", form=form)

def user_logout():
    logout_user()
    return redirect(url_for('index'))

def get_dashboard_homepage():
    modules = []
    module = current_user.get_next_module()
    if module is not None:
        modules.append("cards/_" + module.lower() + "_card.html")
    return render_template('dashboard.html', title="Dashboard", progress=current_user.get_progress(), modules=modules)

def get_learning_homepage():
        # get the learning page, along with the next module to be completed
        modules = []
        modules.append("cards/_alphabet_card.html")
        modules.append("cards/_numbers_card.html")
        modules.append("cards/_greetings_card.html")
        modules.append("cards/_colours_card.html")
        modules.append("cards/_articles_card.html")
        modules.append("cards/_verbs_card.html")
        return render_template('learn.html', title="Learn", modules=modules)

def get_learning_content(content):
    if content == "alphabet":
        return render_template('learning-content/alphabet.html', title="Learn - Alphabet")
    if content == "numbers":
        return render_template('learning-content/numbers.html', title="Learn - Numbers")
    if content == "greetings":
        return render_template('learning-content/greetings.html', title="Learn - Greetings")
    if content == "colours":
        return render_template('learning-content/colours.html', title="Learn - Colours")
    if content == "articles":
        return render_template('learning-content/articles.html', title="Learn - Definite and Indefinite Articles")
    if content == "verbs":
        return render_template('learning-content/verbs.html', title="Learn - Common Verbs")

def get_quiz(quiz_type):
    """
    Renders a quiz page. If the user has already completed this quiz, then the corresponsding quiz form
    will be populated with the user's answers.

    Args:
        quiz_type (str): the type of quiz to be rendered.
    """

    # get the questions for the requested quiz and generate the corresponding quiz form
    quiz = Quiz.query.filter_by(name=quiz_type).first()
    questions = quiz.get_questions()
    form = _generate_quiz_form(questions)

    name = quiz.name
    completed = False
    results = None
    # retrieve user's attempt at the current quiz
    prev_attempt = UserAnswer.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).first()
    if prev_attempt is not None:
        completed = True

        # populate the form with the user's answers
        user_answers = prev_attempt.get_user_answers()
        _populate_form(form, user_answers)

        # construct object to be used to display the correct answers
        solutions = quiz.get_solutions()
        results = _construct_solution(form, solutions)
        user_answers = _retrieve_answers(form)

    elif form.validate_on_submit():
        # get the user's submitted answers
        user_answers = _retrieve_answers(form)

        # get the quiz solution
        solutions = quiz.get_solutions()

        # calculate the user's score
        score = _calculate_quiz_score(user_answers, solutions)

        # add the user's answers to the db
        completed = True
        results = _construct_solution(form, solutions)
        attempt = UserAnswer(quiz_id=quiz.id, 
                            user_id=current_user.id,
                            ans1=user_answers["answer1"]["value"], 
                            ans2=user_answers["answer2"]["value"], 
                            ans3=user_answers["answer3"]["value"], 
                            ans4=user_answers["answer4"]["value"],
                            ans5=user_answers["answer5"]["value"] if "answer5" in user_answers else None,
                            ans6=user_answers["answer6"]["value"] if "answer6" in user_answers else None,
                            ans7=user_answers["answer7"]["value"] if "answer7" in user_answers else None,
                            ans8=user_answers["answer8"]["value"] if "answer8" in user_answers else None,
                            score=score
                        )
        db.session.add(attempt)
        db.session.commit()
    return render_template('quiz/quiz_template.html', title="Quiz - " + name, heading= name + " Quiz", form=form, completed=completed, results=results)

def _populate_form(form, user_answers):
    """
    Helper function for get_quiz.
    Populates a quiz form with the user's answers.

    Args:
       form (QuizForm): an quiz form object with empty input fields
       user_answers (list): a list containing the user's answers for a given quiz, where the ith entry corresponds to the answer to the ith question
        in the form.
    """

    answer = 0
    for question in form:
        if question.type == "StringField":
            question.data = user_answers[answer]
            answer+=1
        elif question.type == "RadioField":
            question.data = user_answers[answer]
            answer+=1
        elif question.type == "IntegerField":
            question.data = user_answers[answer]
            answer+=1
        elif question.type == "MultiCheckboxField":
            question.data = [str(j) for j in range(len(user_answers[answer])) if user_answers[answer][j] == "1"]
            answer+=1

def _construct_solution(form, solutions):
    """
    Helper function which constructs the results dictionary passed to the html page.
    form — a FlaskForm object
    solutions — a list containing the solutions to a given quiz, where the ith entry is the solution to the ith question
    """
    results = {}
    solution_index = 0
    for question in form:
        field = "question"+str(solution_index+1)
        results[field] = {}
        if question.type == "StringField":
            results[field]["is_correct"] = str(question.data).lower() == solutions[solution_index]
            results[field]["solution"] = solutions[solution_index]
            solution_index += 1
        elif question.type == "RadioField":
            results[field]["is_correct"] = question.data == str(solutions[solution_index])
            results[field]["solution"] = str(solutions[solution_index])
            solution_index += 1
        elif question.type == "IntegerField":
            results[field]["is_correct"] = int(question.data) == int(solutions[solution_index])
            results[field]["solution"] = solutions[solution_index]
            solution_index += 1
        elif question.type == "MultiCheckboxField":
            user_answer = "".join(["1" if str(i) in question.data else "0" for i in range(len(solutions[solution_index]))])
            results[field]["solution"] = [True if user_answer[i] == solutions[solution_index][i] else False for i in range(len(solutions[solution_index]))]
            solution_index += 1
    return results

def _retrieve_answers(form):
    """
    Helper function for get_quiz.
    Retrieves the user's answers from a quiz form and puts them into a dictionary.

    Args:
        form (QuizForm): a QuizForm object containing the user's answers for a given quiz.
    
    Returns:
        answers (dict): a dictionary of dictionaries, where each entry of the dictionary corresponds to
            an answer to single quiz question. Each answer dictionary has two fields:
                "type" (str): the form input field type (one of String, Radio, Integer or Checkbox.)
                "value" (str): the user's answer. In the case of a String or Integer Field, it is just simply 
                    the field input. If it is a Radio Field then it is a string corresponding to the selected
                    choice's index. If is is a MultiCheckboxField then it is a binary string corresponding
                    to which choices were selected. 
    """
    answers = {}
    i = 0
    for question in form:
        if question.type == "SubmitField" or question.type == "CSRFTokenField":
            continue
        answer = "answer"+str(i+1)
        answers[answer] = {}
        answers[answer]["type"] = question.type
        if question.type == "StringField":
            answers[answer]["value"] = str(question.data.strip())
        elif question.type == "RadioField":
            answers[answer]["value"] = str(question.data)
        elif question.type == "IntegerField":
            answers[answer]["value"] = str(question.data)
        elif question.type == "MultiCheckboxField":
            answers[answer]["value"] = "".join(["1" if str(j) in question.data else "0" for j in range(len(question.choices))])
        i += 1
    return answers

def _calculate_quiz_score(user_answers, solutions):
    """
    Helper function for get_quiz.
    Calculates a user's score for a given quiz.

    Args:
        user_answers (dict):
        solutions (list): a list containing the solutions to a specific quiz

    Returns:
        score (float): the user's score for the quiz (between 0.0 and 1.0)
    """
    score = 0
    for answer, solution in zip(user_answers, solutions):
        if user_answers[answer]["type"] == "StringField" and user_answers[answer]["value"].lower() == solution:
            score +=1
        elif user_answers[answer]["type"] == "RadioField" and user_answers[answer]["value"] == solution:
            score +=1
        elif user_answers[answer]["type"] == "IntegerField" and user_answers[answer]["value"] == solution:
            score +=1
        elif user_answers[answer]["type"] == "MultiCheckboxField":
            score += sum([0.25 if user_answers[answer]["value"][i] == solution[i] else 0 for i in range(len(solution))])
    score /= len(solutions)
    return score

def _generate_quiz_form(questions):
    """
    Helper function for get_quiz.
    Generates a quiz form for a given quiz.

    Args:
        questions (dict): dictionary of dictionaries, each entry of the top-level dictionary corresponds to
            a quiz question. The children dictionary contains the fields "text", "type" and "choices" for that 
            question. 
                "text" (str): the question text.
                "type" (str): the required form input field type (one of String, Radio, Integer or Checkbox.)
                "choices" (list): a list containing the choices for a multichoice question. (For string and integer
                    type questions this is an empty list.) Each entry of this list is a tuple where
                    the first element corresponds to the index of the choice and the second is the
                    text of the choice.
                    
    Returns:
        a QuizForm() object. 
    """
    # reset quiz form
    for attr, value in QuizForm().__dict__.items():
        if attr[:-1] == "question":
            delattr(QuizForm, attr)
    
    for question in questions:
        if questions[question]["type"] == "String":
            setattr(QuizForm, question, StringField(questions[question]["text"], validators=[DataRequired(), Length(max=20)]))
        elif questions[question]["type"] == "Radio":
            setattr(QuizForm, question, RadioField(questions[question]["text"], choices=questions[question]["choices"], validators=[DataRequired()]))
        elif questions[question]["type"] == "Integer":
            setattr(QuizForm, question, IntegerField(questions[question]["text"], validators=[DataRequired(), NumberRange(min=0,max=999)]))
        elif questions[question]["type"] == "Checkbox":
            setattr(QuizForm, question, MultiCheckboxField(questions[question]["text"], choices=questions[question]["choices"]))    
    return QuizForm()

def get_results():
    # get the names of all quizzes
    all_quizzes = Quiz.query.all()
    labels = []
    if all_quizzes is not None:
        labels = [quiz.name for quiz in all_quizzes]
    
    # calculate the user score for each quiz
    scores = [0 for i in range(len(labels))]
    if all_quizzes is not None:
        for quiz, i in zip(all_quizzes, range(len(labels))):
            # check if the user has completed the current quiz
            user_quiz = UserAnswer.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).first()
            # if so, set the corresponding element in the score list to their score
            if user_quiz is not None:
                scores[i] = round(user_quiz.score * 100)
    return render_template('results.html', title="Results", labels=labels, scores=scores)
