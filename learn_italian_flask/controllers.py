from learn_italian_flask import app
from learn_italian_flask import db
from flask import render_template, redirect, url_for, flash
from learn_italian_flask.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from learn_italian_flask.models import User, AlphabetQuiz, NumbersQuiz
from learn_italian_flask.forms import AlphabetQuizForm, NumbersQuizForm



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
        # TODO pass all card templates similar to how the dashboard does
        return render_template('learn.html', title="Learn")

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

        # def get_alphabet_content():
        #     return render_template('alphabet.html', title="Learn - Alphabet")
        
        # def get_numbers_content():
        #     return render_template('numbers.html', title="Learn - Numbers")
        
        # def get_greetings_content():
        #     return render_template('greetings.html', title="Learn - Greetings")

class QuizController():
    # TODO current problem: question 1 is not being disabled and the other fields are disabled
    #   even if no attempt has been made yet
    #   solution could be to disable it in the html; even if this is removed by client it wont actually cause any changes in the database
    def get_alphabet_quiz():
        form = AlphabetQuizForm()
        completed = False
        prev_attempt = AlphabetQuiz.query.filter_by(testee_id=current_user.id).first()
        results = None
        if prev_attempt is not None:
            completed = True

            # populate the form with the user's answers
            user_answers = prev_attempt.get_answers()
            QuizController.populate_form(form, user_answers)

            # for debugging
            print(prev_attempt.q1, prev_attempt.q2, prev_attempt.q3, prev_attempt.q4)

            # construct object to be used to display the correct answers
            sol = AlphabetQuiz.query.filter_by(id=1).first()
            solutions = sol.get_answers()
            results = QuizController.construct_solution(form, solutions)

        elif form.validate_on_submit():
            # get the user's submitted answers
            user_answers = QuizController.retrieve_answers(form)

            # get the quiz solution
            sol = AlphabetQuiz.query.filter_by(id=1).first()
            
            # calculate the user's score
            score = QuizController.calculate_quiz_score(user_answers, sol.get_answers())

            # # for debugging only
            # ans1_correct = answer1 == sol.q1
            # ans2_correct = answer2 == sol.q2
            # ans3_correct = bin_ans3 == sol.q3
            # ans4_correct = bin_ans4 == sol.q4

            # print(answer1, answer2, bin_ans3, bin_ans4)
            # print(sol.q1, sol.q2, sol.q3, sol.q4)
            # # print(ans1_correct, ans2_correct, ans3_correct, ans4_correct)
            # print(score)
            # # debugging end

            # add the user's attempt to the database
            attempt = AlphabetQuiz(testee_id=current_user.id, q1=user_answers["answer1"]["value"], q2=user_answers["answer2"]["value"], q3=user_answers["answer3"]["value"], q4=user_answers["answer4"]["value"], score=score)
            db.session.add(attempt)
            db.session.commit()
        return render_template("quiz/quiz_template.html", title="Quiz - Alphabet", heading="Alphabet Quiz", form=form, completed=completed, results=results)

    def get_numbers_quiz():
        form = NumbersQuizForm()
        completed = False
        prev_attempt = NumbersQuiz.query.filter_by(testee_id=current_user.id).first()
        results = None
        if prev_attempt is not None:
            completed = True

            # populate the form with the user's answers
            user_answers = prev_attempt.get_answers()
            QuizController.populate_form(form, user_answers)

            # for debugging
            print(prev_attempt.q1, prev_attempt.q2, prev_attempt.q3, prev_attempt.q4)

            # get the quiz solution
            sol =  NumbersQuiz.query.filter_by(id=1).first()
            solutions = sol.get_answers()
            results = QuizController.construct_solution(form, solutions)

        elif form.validate_on_submit():
            # get the user's submitted answers
            user_answers = QuizController.retrieve_answers(form)

            # get the quiz solution
            sol = NumbersQuiz.query.filter_by(id=1).first()

            # calculate the user's score
            score = QuizController.calculate_quiz_score(user_answers, sol.get_answers())

            # # for debugging only
            # ans1_correct = answer1 == sol.q1
            # ans2_correct = answer2.lower() == sol.q2
            # ans3_correct = answer3 == sol.q3
            # ans4_correct = answer4.lower() == sol.q4

            # print(answer1, answer2, answer3, answer4)
            # print(sol.q1, sol.q2, sol.q3, sol.q4)
            # # print(ans1_correct, ans2_correct, ans3_correct, ans4_correct)
            # print(score)
            # # debugging end

            # add the user's attempt to the database
            attempt = NumbersQuiz(testee_id=current_user.id, q1=user_answers["answer1"]["value"], q2=user_answers["answer2"]["value"], q3=user_answers["answer3"]["value"], q4=user_answers["answer4"]["value"], score=score)
            db.session.add(attempt)
            db.session.commit()
        return render_template('quiz/quiz_template.html', title="Quiz - Numbers", heading="Numbers Quiz", form=form, completed=completed, results=results)

    def populate_form(form, user_answers):
        """
        Helper function that populates a quiz form with the user's answers.
        """
        for question, answer in zip(form, user_answers):
            if question.type == "StringField":
                question.data = answer
            elif question.type == "RadioField":
                question.data = str(answer)
            elif question.type == "IntegerField":
                question.data = answer
            elif question.type == "MultiCheckboxField":
                question.data = [str(i) for i in range(len(answer)) if answer[i] == "1"]

    def construct_solution(form, solutions):
        """
        Helper function which constructs the results dictionary passed to the html page.
        """
        results = {}
        for solution, question, i in zip(solutions, form, range(len(solutions))):
            field = "question"+str(i+1)
            results[field] = {}
            if question.type == "StringField":
                results[field]["is_correct"] = question.data.lower() == solution
                results[field]["solution"] = solution
            elif question.type == "RadioField":
                results[field]["is_correct"] = question.data == str(solution)
                results[field]["solution"] = str(solution)
            elif question.type == "IntegerField":
                results[field]["is_correct"] = int(question.data) == solution
                results[field]["solution"] = solution
            elif question.type == "MultiCheckboxField":
                user_answer = "".join(["1" if str(i) in question.data else "0" for i in range(len(solution))])
                results[field]["solution"] = [True if user_answer[i] == solution[i] else False for i in range(len(solution))]
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
            field = "answer"+str(i+1)
            answers[field] = {}
            if question.type == "StringField":
                answers[field]["type"] = "StringField"
                answers[field]["value"] = question.data.strip()
                i += 1
            elif question.type == "RadioField":
                answers[field]["type"] = "RadioField"
                answers[field]["value"] = int(question.data)
                i += 1
            elif question.type == "IntegerField":
                answers[field]["type"] = "IntegerField"
                answers[field]["value"] = question.data
                i += 1
            elif question.type == "MultiCheckboxField":
                answers[field]["type"] = "MultiCheckboxField"
                answers[field]["value"] = "".join(["1" if str(i) in question.data else "0" for i in range(len(question.choices))])
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
