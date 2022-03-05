from re import U
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from pprint import pprint

db = "trips_db"

class Trip:
    def __init__( self , data ):
        self.id = data['id']
        self.destination = data['destination']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.plan = data['plan']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.first_name = data['first_name']
        self.last_name = data['last_name']

        self.users = []
        self.joins = 0

#TODO make get one trip with joiner first name
    @classmethod
    def get_one_trip(cls, data):
        query = """
        SELECT * FROM trips
        WHERE id = %(id)s;"""
        # JOIN users ON trips.user_id = users.id
        results = connectToMySQL(db).query_db(query, data)
        return results[0]

    @classmethod
    def one_trip_with_all_joiners(cls,data):
        query = """
        SELECT * FROM trips
        LEFT JOIN joined_trips ON trips.id = joined_trips.trip_id
        LEFT JOIN users ON users.id = joined_trips.user_id
        WHERE trips.id = %(id)s; """
        results = connectToMySQL(db).query_db(query, data)
        all_joiners = []
        for i in results:
            joiner_info = {
                'id' : i['users.id'],
                'first_name' : i['first_name'],
                'last_name' : i['last_name'],
                'email' : i['email'],
                'password' : i['password'],
                'created_at' : i['users.created_at'],
                'updated_at' : i['users.updated_at']
            }
            if len(all_joiners) == 0:
                all_joiners.append(cls(i))
            if i['id'] and i['id'] != all_joiners[-1].id :
                all_joiners.append(cls(i))
            if i['joined_trips.id'] and len(all_joiners[-1].users) == 0:
                all_joiners[-1].users.append(user.User(joiner_info))
            if i['joined_trips.id'] and all_joiners[-1].users[-1].id != i['users.id']:
                all_joiners[-1].users.append(user.User(joiner_info))
        join = all_joiners[0]
        pprint(i,sort_dicts = False)
        return join

    @classmethod
    def get_all_trips_with_joiners(cls, data):
        query = """
        SELECT * FROM trips
        LEFT JOIN joined_trips ON trips.id = joined_trips.trip_id
        LEFT JOIN users ON users.id = joined_trips.user_id;"""
        results = connectToMySQL(db).query_db(query, data)
        joined_trips = []
        for trip in results:
            joiner_info = {
                "id":trip['users.id'],
                "first_name":trip['first_name'],
                "last_name":trip['last_name'],
                "email":trip['email'],
                "password":trip['password'],
                "created_at":trip['users.created_at'],
                "updated_at":trip['users.updated_at'],
            }
            if len(joined_trips) == 0:
                joined_trips.append(cls(trip))
                # pprint(f"this is my first trip {joined_trips}")
            if trip['joined_trips.id'] and len(joined_trips[-1].users) == 0:
                joined_trips[-1].users.append(user.User(joiner_info))
                # pprint(f"this is my trips first joiner {joined_trips[-1].users}")
            if trip['trip_id'] and joined_trips[-1].users[-1] != trip['users.id']:
                joined_trips[-1].users.append(user.User(joiner_info))
                # pprint(f"this is my trips other joiner {joined_trips[-1].users}")
            if trip['id'] and trip['id'] != joined_trips[-1].id:
                joined_trips.append(cls(trip))
                # pprint(f"this is my next trip {joined_trips[-1]}")
            # pprint(trip,sort_dicts = False)
        return joined_trips

    @classmethod
    def user_that_joined_trip(cls, data):
        query = """
        SELECT * FROM trips
        JOIN joined_trips ON joined_trips.trip_id = trips.id
        JOIN users on users.id = joined_trips.user_id;"""
        results = connectToMySQL(db).query_db(query, data)
        joined_users = []
        for trip in results:
            joined_users.append(trip)
        return joined_users

    @classmethod
    def join_trip(cls, data):
        query="""
        INSERT INTO joined_trips (trip_id, user_id)
        VALUES (%(trip_id)s, %(user_id)s);"""
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def all_trips_not_joined(cls,data):
        query = """
        SELECT * FROM trips
        WHERE trips.id NOT IN ( SELECT trip_id FROM joined_trips WHERE user_id = %(id)s );"""
        results = connectToMySQL(db).query_db(query,data)
        trips = []
        for row in results:
            trips.append(row)
        return trips

    @classmethod
    def save_trip(cls,data):
        query = """
        INSERT INTO trips (destination, start_date, end_date, plan, user_id)
        VALUES (%(destination)s, %(start_date)s, %(end_date)s, %(plan)s, %(user_id)s);"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update_trip(cls, data):
        query = """
        UPDATE trips
        SET destination=%(destination)s, start_date=%(start_date)s, end_date=%(end_date)s, plan=%(plan)s, user_id=%(user_id)s
        WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def remove_from_joined_trips(cls, data):
        query="DELETE FROM joined_trips WHERE trip_id = %(trip_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy_trip(cls,data):
        query = "DELETE FROM trips WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_trip(quote):
        is_valid = True
        if len(quote['destination']) < 1:
            is_valid = False
            flash("Please enter a destination.","trip")
        if len(quote['start_date']) == "":
            is_valid = False
            flash("Please enter a Start Date.","trip")
        if len(quote['end_date']) == "":
            is_valid = False
            flash("Please enter an End Date.","trip")
        if len(quote['plan']) < 1:
            is_valid = False
            flash("Please enter a plan.","trip")
        return is_valid

    @classmethod
    def get_all_trips_by_one_poster(cls, data):
        query = """
        SELECT * FROM trips
        JOIN users ON users.id = trips.user_id
        WHERE trips.id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        all_trips = []
        for trip in results:
            all_trips.append(cls(trip))
        return all_trips
