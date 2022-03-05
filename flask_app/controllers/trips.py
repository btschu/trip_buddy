from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trip import Trip

@app.route('/trip/new')
def new_trip():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    context = {
        'user' : User.get_by_id(data)
    }
    return render_template('create_trip.html', **context)

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
        "id":session['user_id']
    }
    data = {
        "id":id
    }
    context = {
        "edit" : Trip.get_one_trip(data),
        "user" : User.get_by_id(user_data)
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
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    context = {
        # "trip" : Trip.get_one_trip(data),
        "user" : User.get_by_id(user_data),
        "trips" : Trip.get_all_trips_by_one_poster(data),
        # "joined" : Trip.user_that_joined_trip(data),
        "joined_trip" : Trip.one_trip_with_all_joiners(data),
        "trip_id" : id,
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

@app.route('/joined_trip/destroy/<int:trip_id>/<int:user_id>')
def unjoin_trip(trip_id, user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "trip_id":trip_id,
        "user_id":user_id
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