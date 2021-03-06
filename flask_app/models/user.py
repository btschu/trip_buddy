from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = "trips_db"

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trips = []

    @classmethod
    def save(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query,user)
        if len(user['first_name']) < 1:
            flash("Please enter your FIRST NAME.","register")
            is_valid= False
        if len(user['last_name']) < 1:
            flash("Please enter your LAST NAME","register")
            is_valid= False
        if len(results) >= 1:
            flash("That EMAIL ADDRESS is already registered.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter a valid EMAIL ADDRESS.","login")
            is_valid=False
        if len(user['password']) < 8:
            flash("Your PASSWORD must be at least 8 characters long.","register")
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash("Your PASSWORD must contain at least one number.", "register")
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash("Your PASSWORD must contain at least one uppercase letter.", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Your PASSWORDS do not match.","register")
            is_valid = False
        return is_valid
