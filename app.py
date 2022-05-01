from flask import Flask, render_template, url_for, request, session, redirect, jsonify
import bcrypt
from flask_pymongo import PyMongo
from pymongo import ALL
app = Flask(__name__)

app.config['MONGODB_NAME'] = 'ablejob'
app.config['MONGO_URI'] = 'mongodb_url_to_connect'
app.config['SECRET_KEY'] = b'6hc/_gsh,./;2ZZx3c6_s,1//'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return render_template('index.html')


@app.route('/index')
def main():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        curr_user = users.find_one({'username': request.form['username']})
        if curr_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), curr_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('form'))
            return render_template('login.html')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        curr_user = users.find_one({'username': request.form['username']})
        if curr_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass})
            session['username'] = request.form['username']
            return render_template('form.html')
        return render_template('index.html')
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/form')
def form():
    if 'username' in session:
        return render_template('form.html')
    else:
        return redirect(url_for('login'))


@app.route('/requirement', methods=['POST', 'GET'])
def requirement():
    if 'username' in session and request.method == 'POST':
        company = session['username']
        jobs = mongo.db.jobs
        jobs.insert({'company': company, 'jobRole': request.form['role'], 'jobDescription': request.form[
                    'description'], 'placeOfWork': request.form['work'], 'phone': request.form['phone']})
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/user/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        company = session['username']
        jobs = mongo.db.jobs
        job_list = jobs.find({"company": company})
        return render_template('user_dashboard.html', job_list=job_list)
    return render_template('login.html')


@app.route('/admin/dashboard', methods=['GET'])
def adminDashboard():
    if 'username' in session and session['username'] == "admin":
        jobs = mongo.db.jobs
        all_list = jobs.find()
        return render_template('admin_dashboard.html', all_list=all_list)
    return render_template('login.html')


if __name__ == '__main__':
    # app.secret_key = "hello"
    app.run(debug=True)
