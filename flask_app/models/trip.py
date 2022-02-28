from re import U
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from pprint import pprint

db = "trips_db"

class Trip:
    def __init__( self , data ):
        self.id = data['id']
        self.destination = data['destination']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.first_name = data['first_name']
        self.last_name = data['last_name']

        self.users = []
        self.joins = 0

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
    def get_all_trips(cls):
        query = """
        SELECT * FROM trips;"""
        results = connectToMySQL(db).query_db(query)
        all_trips = []
        for trip in results:
            all_trips.append(trip)
        return all_trips

    @classmethod
    def get_one_trip(cls, data):
        query = """
        SELECT * FROM trips
        WHERE id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        return results[0]

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