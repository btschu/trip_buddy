from re import U
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from pprint import pp, pprint

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
        # self.creator_first_name = data['first_name']
        # self.creator_last_name = data['last_name']
        self.joiners = []
        self.creator = None

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
    def join_trip(cls, data):
        query="""
        INSERT INTO joined_trips (trip_id, user_id)
        VALUES (%(trip_id)s, %(user_id)s);"""
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def remove_from_joined_trips(cls, data):
        query="DELETE FROM joined_trips WHERE trip_id = %(trip_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy_trip(cls,data):
        query = "DELETE FROM trips WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def all_trips_not_joined(cls,data):
        query = """
        SELECT * FROM trips
        WHERE trips.id NOT IN ( SELECT trip_id FROM joined_trips WHERE user_id = %(id)s )
        ORDER BY start_date ASC;"""
        results = connectToMySQL(db).query_db(query,data)
        trips = []
        for row in results:
            trips.append(row)
        return trips

    # @classmethod
    # def get_all_trips_with_joiners(cls, data):
    #     query = """
    #     SELECT * FROM trips
    #     LEFT JOIN joined_trips ON trips.id = joined_trips.trip_id
    #     LEFT JOIN users ON users.id = joined_trips.user_id
    #     ORDER BY start_date ASC;"""
    #     results = connectToMySQL(db).query_db(query, data)
    #     this_joined_trip = cls(results[0])
    #     joined_trip_info = {
    #         "id":results[0]['joined_trips.id'],
    #         "user_id":results[0]['joined_trips.user_id'],
    #         "trip_id":results[0]['trip_id'],
    #         "created_at":results[0]['joined_trips.created_at'],
    #         "updated_at":results[0]['joined_trips.updated_at'],
    #     }
    #     this_joiner = joined_trip_info
    #     this_joined_trip.joiners = this_joiner
    #     joined_trips = []
    #     for trip in results:
    #         joiner_info = {
    #             "id":trip['users.id'],
    #             "first_name":trip['first_name'],
    #             "last_name":trip['last_name'],
    #             "email":trip['email'],
    #             "password":trip['password'],
    #             "created_at":trip['users.created_at'],
    #             "updated_at":trip['users.updated_at'],
    #         }
    #         if trip['users.id'] != None:
    #             this_joiner.joiners.append(user.User(joiner_info))
    #     return this_joined_trip

    @classmethod
    def get_all_trips_with_joiners(cls, data):
        query = """
        SELECT * FROM trips
        LEFT JOIN joined_trips ON trips.id = joined_trips.trip_id
        LEFT JOIN users ON users.id = joined_trips.user_id
        ORDER BY start_date ASC;"""
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
            if trip['id'] and trip['id'] != joined_trips[-1].id:
                joined_trips.append(cls(trip))
            if trip['joined_trips.id'] and len(joined_trips[-1].joiners) == 0:
                joined_trips[-1].joiners.append(user.User(joiner_info))
            if trip['trip_id'] and joined_trips[-1].joiners[-1] != trip['users.id']:
                joined_trips[-1].joiners.append(user.User(joiner_info))
            pprint(trip,sort_dicts = False)
        return joined_trips

    @classmethod
    def get_one_trip(cls, data):
        query = """
        SELECT * FROM trips
        JOIN users ON trips.user_id = users.id
        WHERE trips.id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        creator_info = {
            "id":results[0]['users.id'],
            "first_name":results[0]['first_name'],
            "last_name":results[0]['last_name'],
            "email":results[0]['email'],
            "password":results[0]['password'],
            "created_at":results[0]['users.created_at'],
            "updated_at":results[0]['users.updated_at']
        }
        this_trip = cls(results[0])
        this_trip.creator = user.User(creator_info)
        # pprint(this_trip)
        # pprint(this_trip.creator)
        return this_trip

    @classmethod
    def user_that_joined_trip(cls, data):
        query = """
        SELECT first_name AS joiner_first_name, last_name AS joiner_last_name FROM users
        JOIN joined_trips ON joined_trips.user_id = users.id
        JOIN trips on trips.id = joined_trips.trip_id
        WHERE trips.id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        joined_users = []
        for trip in results:
            joined_users.append(trip)
        pprint(joined_users)
        return joined_users

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
