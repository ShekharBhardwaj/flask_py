import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username is a required field to sign up!")
    parser.add_argument('password', type=str, required=True, help="please enter the password to sign up!")

    def post(self):
        payload = UserRegister.parser.parse_args()
        if UserModel.find_by_username(payload['username']):
            return {"message": "user already exists"}, 400
        # connection = sqlite3.connect("users.db")
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (payload['username'], payload['password']))
        # connection.commit()
        # connection.close()
        user = UserModel(**payload)
        user.save_to_db()
        return {'message': "User was created successfully."}, 201
