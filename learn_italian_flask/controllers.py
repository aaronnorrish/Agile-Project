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
    return render_template('index.html', title="Learn Italian")

def get_statistics():
    all_user_quizzes = UserAnswer.query.all()
    num_quizzes_completed = sum([1 for quiz in all_user_quizzes])
    print(num_quizzes_completed)
    all_quizzes = Quiz.query.all()

    labels = []
    if all_quizzes is not None:
        labels = [quiz.name for quiz in all_quizzes]
    cumulative_scores = [0 for i in range(len(labels))]
    attempts = [0 for i in range(len(labels))]
    for quiz in all_user_quizzes:
        cumulative_scores[quiz.quiz_id-1] += quiz.score * 100
        attempts[quiz.quiz_id-1] += 1
    scores = [round(score/attempt) if attempt != 0 else 0 for score, attempt in zip(cumulative_scores, attempts)]

    users = User.query.all()
    num_users = sum([1 for user in users])
    print(num_users)
    return render_template('statistics.html', title="Learn Italian — Usage Statistics", labels=labels, scores=scores, num_users=num_users, num_quizzes_completed=num_quizzes_completed)


def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('log-in.html', title="Learn Italian - Log in", form=form)

def user_signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('sign-up.html', title="Learn Italian - Sign up", form=form)

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
        return render_template('alphabet.html', title="Learn - Alphabet")
    if content == "numbers":
        return render_template('numbers.html', title="Learn - Numbers")
    if content == "greetings":
        return render_template('greetings.html', title="Learn - Greetings")
    if content == "colours":
        return render_template('colours.html', title="Learn - Colours")
    if content == "articles":
        return render_template('articles.html', title="Learn - Definite and Indefinite Articles")
    if content == "verbs":
        return render_template('verbs.html', title="Learn - Common Verbs")

def get_quiz(quiz_type):
    quiz = Quiz.query.filter_by(name=quiz_type).first()
    questions = quiz.get_questions()
    name = quiz.name
    form = _generate_quiz_form(questions)

    completed = False
    prev_attempt = UserAnswer.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).first()
    results = None
    if prev_attempt is not None:
        completed = True

        # populate the form with the user's answers
        user_answers = prev_attempt.get_user_answers()
        _populate_form(form, user_answers)

        # construct object to be used to display the correct answers
        solutions = quiz.get_solutions()
        results = _construct_solution(form, solutions)
        user_answers = _retrieve_answers(form)
        print(user_answers)

    elif form.validate_on_submit():
        # get the user's submitted answers
        user_answers = _retrieve_answers(form)

        # get the quiz solution
        solutions = quiz.get_solutions()

        # calculate the user's score
        score = _calculate_quiz_score(user_answers, solutions)
        print(user_answers)

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
    Helper function that populates a quiz form with the user's answers.
    form — a FlaskForm object
    user_answers — a list containing the user's answers for a given quiz, where the ith entry corresponds to the answer to the ith question
        in the form
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
    Helper function which retrieves the user's answers from a form and puts them into a dictionary.
    Each entry of the dictionary contains a type (corresponding to the form field type for that question)
    and a value (the answer itself.)
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
    Helper function that calculates a user's score for a given quiz.
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

"""
Helper function that generates a quiz form for a given quiz.
questions — dictionary of dictionaries, each with fields "text", "type" and "choices"
"""
def _generate_quiz_form(questions):
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
    all_quizzes = Quiz.query.all()
    labels = []
    if all_quizzes is not None:
        labels = [quiz.name for quiz in all_quizzes]
    scores = [0 for i in range(len(labels))]
    if all_quizzes is not None:
        for quiz, i in zip(all_quizzes, range(len(labels))):
            user_quiz = UserAnswer.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).first()
            if user_quiz is not None:
                scores[i] = round(user_quiz.score * 100)
    return render_template('results.html', title="Results", labels=labels, scores=scores)
