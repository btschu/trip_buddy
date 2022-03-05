from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trip import Trip
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Login to site

@app.route('/')
def login():
    return render_template('login.html')

@app.route("/login",methods=['POST'])
def user_login():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/dashboard')

# Register new user

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/registration')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

# Dashboard

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        'first_name': session['first_name']
    }
    context = {
        "user" : User.get_by_id(data),
        "trips_not_joined" : Trip.all_trips_not_joined(data),
        "joined_trips" : Trip.get_all_trips_with_joiners(data)
    }
    return render_template("dashboard.html", **context)

# Edit user

# @app.route('/account/edit/<int:id>')
# def edit_account(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     user_data = {
#         "id":session['user_id']
#     }
#     context = {
#         "edit" : User.get_by_id(user_data),
#     }
#     return render_template("edit_account.html", **context)

# @app.route('/account/update',methods=['POST'])
# def update_account():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     user_id = request.form['id']
#     if not User.validate_edit_user(request.form):
#         return redirect(f'/account/edit/{user_id}')
#     data = {
#         "id": session["user_id"],
#         "first_name": request.form["first_name"],
#         "last_name": request.form["last_name"],
#         "email": request.form["email"]
#     }
#     User.update(data)
#     return redirect('/dashboard')

# Logout

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')