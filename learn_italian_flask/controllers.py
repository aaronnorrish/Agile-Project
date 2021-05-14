from learn_italian_flask import app
from learn_italian_flask import db
from flask import render_template, redirect, url_for, flash
from learn_italian_flask.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User, AlphabetQuiz, NumbersQuiz, Quiz, UserAnswer
from learn_italian_flask.forms import AlphabetQuizForm, NumbersQuizForm, QuizForm, MultiCheckboxField

# test
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectMultipleField, widgets
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length, NumberRange



class UserController():
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        # TODO haven't added a flash error as in the tutorial
        # if want to render the flash messages need to add this to the HTML template
        # as in the chapter 3 of the tutorial
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('dashboard'))
        return render_template('log-in.html', title="Learn Italian - Log in", form=form)
    
    def signup():
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
    
    def logout():
        logout_user()
        return redirect(url_for('index'))

# TODO should be in the UserController class instead??
class DashboardController():
    def get_dashboard_homepage():
        modules = []
        if current_user.get_next_module() == "alphabet":
            modules.append("cards/_alphabet_card.html")
        elif current_user.get_next_module() == "numbers":
            modules.append("cards/_numbers_card.html")
        return render_template('dashboard.html', title="Dashboard", progress=current_user.get_progress(), modules=modules)

class LearnController():
    def get_learn_homepage():

        modules = []
        modules.append("cards/_alphabet_card.html")
        modules.append("cards/_numbers_card.html")
        modules.append("cards/_greetings_card.html")
        modules.append("cards/_colours_card.html")
        modules.append("cards/_articles_card.html")
        modules.append("cards/_verbs_card.html")
        return render_template('learn.html', title="Learn", modules=modules)

    def get_content(content):
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

class QuizController():
    # TODO current problem: question 1 is not being disabled and the other fields are disabled
    #   even if no attempt has been made yet
    #   solution could be to disable it in the html; even if this is removed by client it wont actually cause any changes in the database
    def get_quiz(quiz_type):
        # quizzes = Quiz.query.all()
        # for quiz in quizzes:
        #     print(quiz.name)
        quiz = Quiz.query.filter_by(name=quiz_type).first()
        questions = quiz.get_questions()
        name = quiz.name
        form = QuizController.generate_quiz_form(questions)
        print(form)

        completed = False
        prev_attempt = UserAnswer.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).first()
        results = None
        if prev_attempt is not None:
            completed = True

            # # populate the form with the user's answers
            user_answers = prev_attempt.get_user_answers()
            print(user_answers)
            QuizController.populate_form(form, user_answers)

            # construct object to be used to display the correct answers
            solutions = quiz.get_solutions()
            results = QuizController.construct_solution(form, solutions)

        elif form.validate_on_submit():
            # get the user's submitted answers
            user_answers = QuizController.retrieve_answers(form)

            # get the quiz solution
            solutions = quiz.get_solutions()

            # calculate the user's score
            score = QuizController.calculate_quiz_score(user_answers, solutions)
            print(score)

            completed = True
            results = QuizController.construct_solution(form, solutions)
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

    def populate_form(form, user_answers):
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

    def construct_solution(form, solutions):
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

    def retrieve_answers(form):
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
    
    def calculate_quiz_score(user_answers, solutions):
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
    def generate_quiz_form(questions):
        name = "question"
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

class ResultsController():
    def get_results():
        labels = ['Alphabet', 'Numbers', 'Greetings', 'Colours', 'Articles', 'Common Verbs']
        scores = [0 for i in range(6)]
        alphabet_quiz = AlphabetQuiz.query.filter_by(testee_id=current_user.id).first()
        if alphabet_quiz is not None:
            scores[0] = alphabet_quiz.score * 100
        numbers_quiz = NumbersQuiz.query.filter_by(testee_id=current_user.id).first()
        if numbers_quiz is not None:
            scores[1] = numbers_quiz.score * 100
        return render_template('results.html', title="Results", labels=labels, scores=scores)
