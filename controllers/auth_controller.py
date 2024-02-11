from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("/register", methods=["POST"]) # /auth/register
def auth_register():
    try:
        # The data that we get in the body of the request
        body_data = request.get_json()
        # password from the request body
        password = body_data.get('password')
        hashed_password = ""
        # If passwor exists, pass the password
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # create the user interface
        user = User(
            name=body_data.get('name'),
            email=body_data.get('email'),
            password=hashed_password
        )

        #add and commit the user to db
        db.session.add(user)
        db.session.commit()
        # Respond back to the client
        return user_schema.dump(user), 201

    except Exception as e:
        raise e