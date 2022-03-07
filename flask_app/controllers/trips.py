from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trip import Trip

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        'first_name': session['first_name']
    }
    context = {
        "trips_not_joined" : Trip.all_trips_not_joined(data),
        # "joined_trips" : Trip.all_trips_joined(data),
        # "joiner" : Trip.user_that_joined_trip(data)
        "joined_trips" : Trip.get_all_trips_with_joiners(data)
    }
    return render_template("dashboard.html", **context)

@app.route('/trip/new')
def new_trip():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id'],
        'first_name': session['first_name']
    }
    return render_template('create_trip.html')

@app.route('/trip/create',methods=['POST'])
def create_trip():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Trip.validate_trip(request.form):
        return redirect('/trip/new')
    data = {
        "destination": request.form["destination"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"],
        "plan": request.form["plan"],
        "user_id": session["user_id"]
    }
    Trip.save_trip(data)
    return redirect('/dashboard')

@app.route('/trip/edit/<int:id>')
def edit_trip(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id'],
        'first_name': session['first_name']
    }
    data = {
        "id":id
    }
    context = {
        "edit" : Trip.get_one_trip(data),
    }
    return render_template("edit_trip.html", **context)

@app.route('/trip/update',methods=['POST'])
def update_trip():
    if 'user_id' not in session:
        return redirect('/logout')
    trip_id = request.form['id']
    if not Trip.validate_trip(request.form):
        return redirect(f'/trip/edit/{trip_id}')
    data = {
        "id": request.form['id'],
        "destination": request.form["destination"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"],
        "plan": request.form["plan"],
        "user_id": session['user_id']
    }
    Trip.update_trip(data)
    return redirect('/dashboard')

@app.route('/trip/view/<int:id>')
def view_trip(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
        "user_id":session['user_id'],
        'first_name': session['first_name'],
        'last_name': session['last_name'],
    }
    context = {
        "joined" : Trip.user_that_joined_trip(data),
        "trip" : Trip.get_one_trip(data),
    }
    return render_template("view_trip.html", **context)

@app.route('/join/trip/<int:trip_id>')
def join_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'trip_id': trip_id,
        'user_id': session['user_id']
    }
    Trip.join_trip(data)
    return redirect("/dashboard")

@app.route('/unjoin_trip/<int:trip_id>')
def unjoin_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "trip_id":trip_id,
        "user_id":session['user_id']
    }
    Trip.remove_from_joined_trips(data)
    return redirect('/dashboard')

@app.route('/trip/destroy/<int:id>')
def destroy_trip(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Trip.destroy_trip(data)
    return redirect('/dashboard')