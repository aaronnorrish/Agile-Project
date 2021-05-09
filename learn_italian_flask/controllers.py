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
        print(current_user.get_progress())
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
        solution = None
        if prev_attempt is not None:
            completed = True

            # populate the form with the user's answers
            form.question1.data = prev_attempt.q1
            form.question2.data = str(prev_attempt.q2)
            form.question3.data = [str(i) for i in range(len(prev_attempt.q3)) if prev_attempt.q3[i] == "1"]
            form.question4.data = [str(i) for i in range(len(prev_attempt.q4)) if prev_attempt.q4[i] == "1"]
            
            # for debugging
            print(prev_attempt.q1, prev_attempt.q2, prev_attempt.q3, prev_attempt.q4)

            # get the quiz solution
            solution = AlphabetQuiz.query.filter_by(id=1).first()

            # construct object to be used to display the correct answers
            sol_q3 = [True if prev_attempt.q3[i] == solution.q3[i] else False for i in range(len(prev_attempt.q3))]
            sol_q4 = [True if prev_attempt.q4[i] == solution.q4[i] else False for i in range(len(prev_attempt.q4))]

            solution = {"question1": {"is_correct": solution.q1 == prev_attempt.q1, "solution": solution.q1},
                        "question2": {"is_correct": solution.q2 == prev_attempt.q2, "solution": solution.q2},
                        "question3": {"solution": sol_q3},
                        "question4": {"solution": sol_q4}}

        elif form.validate_on_submit():
            # get the user's submitted answers
            answer1 = form.question1.data
            answer2 = int(form.question2.data)
            answer3 = form.question3.data
            answer4 = form.question4.data

            # convert checkbox selections into a binary string
            bin_ans3 = "".join(["1" if str(i) in answer3 else "0" for i in range(4)])
            bin_ans4 = "".join(["1" if str(i) in answer4 else "0" for i in range(4)])

            # get the quiz solution
            sol = AlphabetQuiz.query.filter_by(id=1).first()
            
            # calculate the user's score
            score = 0
            score = score + 1 if answer1 == sol.q1 else score
            score = score + 1 if answer2 == sol.q2 else score
            score += sum([0.25 if bin_ans3[i] == sol.q3[i] else 0 for i in range(4)])
            score += sum([0.25 if bin_ans4[i] == sol.q4[i] else 0 for i in range(4)])
            score /= 4

            # for debugging only
            ans1_correct = answer1 == sol.q1
            ans2_correct = answer2 == sol.q2
            ans3_correct = bin_ans3 == sol.q3
            ans4_correct = bin_ans4 == sol.q4

            print(answer1, answer2, bin_ans3, bin_ans4)
            print(sol.q1, sol.q2, sol.q3, sol.q4)
            # print(ans1_correct, ans2_correct, ans3_correct, ans4_correct)
            print(score)
            # debugging end

            # add the user's attempt to the database
            attempt = AlphabetQuiz(testee_id=current_user.id, q1=answer1, q2=answer2, q3=bin_ans3, q4=bin_ans4, score=score)
            db.session.add(attempt)
            db.session.commit()
        return render_template("quiz/quiz_template.html", title="Quiz - Alphabet", heading="Alphabet Quiz", form=form, completed=completed, solution=solution)

    def get_numbers_quiz():
        form = NumbersQuizForm()
        completed = False
        prev_attempt = NumbersQuiz.query.filter_by(testee_id=current_user.id).first()
        solution = None
        if prev_attempt is not None:
            completed = True

            # populate the form with the user's answers
            form.question1.data = str(prev_attempt.q1)
            form.question2.data = prev_attempt.q2
            form.question3.data = str(prev_attempt.q3)
            form.question4.data = prev_attempt.q4

            # for debugging
            print(prev_attempt.q1, prev_attempt.q2, prev_attempt.q3, prev_attempt.q4)

            # get the quiz solution
            solution =  NumbersQuiz.query.filter_by(id=1).first()

            solution = {
                "question1": {"is_correct": solution.q1 == prev_attempt.q1, "solution": solution.q1},
                "question2": {"is_correct": solution.q2 == prev_attempt.q2.lower(), "solution": solution.q2},
                "question3": {"is_correct": solution.q3 == prev_attempt.q3, "solution": solution.q3},
                "question4": {"is_correct": solution.q4 == prev_attempt.q4.lower(), "solution": solution.q4}
            }


        elif form.validate_on_submit():
            # get the user's submitted answers
            # strip white space from string input
            answer1 = int(form.question1.data)
            answer2 = form.question2.data.strip()
            answer3 = int(form.question3.data)
            answer4 = form.question4.data.strip()

            # get the quiz solution
            sol = NumbersQuiz.query.filter_by(id=1).first()

            # calculate the user's score
            score = 0
            score = score + 1 if answer1 == sol.q1 else score
            score = score + 1 if answer2.lower() == sol.q2 else score
            score = score + 1 if answer3 == sol.q3 else score
            score = score + 1 if answer4.lower() == sol.q4 else score
            score /= 4

            # for debugging only
            ans1_correct = answer1 == sol.q1
            ans2_correct = answer2.lower() == sol.q2
            ans3_correct = answer3 == sol.q3
            ans4_correct = answer4.lower() == sol.q4

            print(answer1, answer2, answer3, answer4)
            print(sol.q1, sol.q2, sol.q3, sol.q4)
            # print(ans1_correct, ans2_correct, ans3_correct, ans4_correct)
            print(score)
            # debugging end

            # add the user's attempt to the database
            attempt = NumbersQuiz(testee_id=current_user.id, q1=answer1, q2=answer2, q3=answer3, q4=answer4, score=score)
            db.session.add(attempt)
            db.session.commit()
        return render_template('quiz/quiz_template.html', title="Quiz - Numbers", heading="Numbers Quiz", form=form, completed=completed, solution=solution)

