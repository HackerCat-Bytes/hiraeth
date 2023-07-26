from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import pandas as pd
from quests import Quest, CSVAccessLayer, DepressionPhase, AnxietyPhase, StressPhase, MentalHealthEvaluation

app = Flask(__name__)

app.config['SECRET_KEY'] = 'coco'

csv_access = CSVAccessLayer('questions.csv')

# Ensure users.csv exists
if not os.path.isfile('users.csv'):
    pd.DataFrame(columns=['id', 'username', 'password', 'email']).to_csv('users.csv', index=False)

# Ensure answers.csv exists
if not os.path.isfile('answers.csv'):
    pd.DataFrame(columns=['id', 'phase', 'question', 'answer']).to_csv('answers.csv', index=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Load user data from CSV
    df = pd.read_csv('users.csv')

    user = df.loc[df['email'] == email].to_dict('records')

    if not user or user[0]['password'] != password:
        flash('Please check your login details and try again.')
        return redirect(url_for('home'))

    session['user_id'] = user[0]['id']

    return redirect(url_for('profile'))

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('username')

    # Load user data from CSV
    df = pd.read_csv('users.csv')

    if email in df['email'].values:
        flash('Email address already exists')
        return redirect(url_for('home'))

    new_id = df['id'].max() + 1 if not df.empty else 0

    new_user = pd.DataFrame([[new_id, name, password, email]], columns=['id', 'username', 'password', 'email'])
    
    # Append new user and save
    df = pd.concat([df, new_user])
    df.to_csv('users.csv', index=False)

    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    # if 'user_id' not in session:
    #     return redirect(url_for('home'))

    df = pd.read_csv('users.csv')

    user = df.loc[df['id'] == session['user_id']].to_dict('records')[0] if 'user_id' in session else None
    depression_score = session.get('depression_score', 'Not available')
    anxiety_score = session.get('anxiety_score', 'Not available')
    stress_score = session.get('stress_score', 'Not available')

    if all([depression_score != 'Not available', anxiety_score != 'Not available', stress_score != 'Not available']):
        depression_phase = session['depression_phase']
        anxiety_phase = session['anxiety_phase']
        stress_phase = session['stress_phase']
        evaluation = MentalHealthEvaluation(depression_phase, anxiety_phase, stress_phase)
        result = evaluation.evaluate()
        total_score = evaluation.calculate_total_score()
    else:
        total_score = 'Not available'
        result = 'Not available'

    return render_template('profile.html', user=user, logged_in='user_id' in session)

@app.route('/depression', methods=['GET', 'POST'])
def depression():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        # handle form submit here
        answer = request.form['answer']
        depression_phase = session['depression_phase']
        depression_phase.answer_question(answer)
        session['depression_phase'] = depression_phase  # save back to session
        if depression_phase.get_next_question() is None:
            session['depression_score'] = depression_phase.calculate_score()
            return redirect(url_for('anxiety'))  # if no more questions, go to the next phase
    else:
        if 'depression_phase' not in session:  # if it's the first visit, create a new phase
            depression_phase = DepressionPhase(session['user_id'], csv_access)
            depression_phase.start_phase()
            session['depression_phase'] = depression_phase
        else:
            depression_phase = session['depression_phase']
    question = depression_phase.get_next_question()
    return render_template('question.html', question=question)

@app.route('/anxiety', methods=['GET', 'POST'])
def anxiety():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        # handle form submit here
        answer = request.form['answer']
        anxiety_phase = session['anxiety_phase']
        anxiety_phase.answer_question(answer)
        session['anxiety_phase'] = anxiety_phase  # save back to session
        if anxiety_phase.get_next_question() is None:
            session['anxiety_score'] = anxiety_phase.calculate_score()
            return redirect(url_for('stress'))  # if no more questions, go to the next phase
    else:
        if 'anxiety_phase' not in session:  # if it's the first visit, create a new phase
            anxiety_phase = AnxietyPhase(session['user_id'], csv_access)
            anxiety_phase.start_phase()
            session['anxiety_phase'] = anxiety_phase
        else:
            anxiety_phase = session['anxiety_phase']
    question = anxiety_phase.get_next_question()
    return render_template('question.html', question=question)

@app.route('/stress', methods=['GET', 'POST'])
def stress():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        # handle form submit here
        answer = request.form['answer']
        stress_phase = session['stress_phase']
        stress_phase.answer_question(answer)
        session['stress_phase'] = stress_phase  # save back to session
        if stress_phase.get_next_question() is None:
            session['stress_score'] = stress_phase.calculate_score()
            return redirect(url_for('profile'))  # if no more questions, go to the profile
    else:
        if 'stress_phase' not in session:  # if it's the first visit, create a new phase
            stress_phase = StressPhase(session['user_id'], csv_access)
            stress_phase.start_phase()
            session['stress_phase'] = stress_phase
        else:
            stress_phase = session['stress_phase']
    question = stress_phase.get_next_question()
    return render_template('question.html', question=question)

if __name__ == '__main__':
    app.run(debug=True)