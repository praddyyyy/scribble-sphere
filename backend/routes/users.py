from routes import app, version, db
from flask import request, jsonify, Response
from models.user_model import Users
import json

from helpers import token_required, token_generate


@app.route(version + '/login', methods=["POST"])
def login():
    # getting login info from the form
    login = {
        "username": request.form["username"],
        "password": request.form["password"]
    }

    # using try catch for sys error and check pass
    try:
        user = Users.query.filter_by(username=login["username"]).first()
        if not user:
            return jsonify({'message': "Invalid Credentials"})
        if user.password == login["password"]:
            token = token_generate(login["username"])

            return jsonify({"token": token}), 200

        else:
            return jsonify({"message": "Invalid Credentials"}), 404

    except:
        return jsonify({"message": "Invalid Credentials"}), 404


@app.route(version + '/signup', methods=["POST"])
def signup():
    # creating a user dict to store the values from the forms
    user = {"fname": request.form["firstName"],
            "lname": request.form["lastName"],
            "email": request.form["email"],
            "username": request.form["username"],
            "bio": request.form["bio"],
            "password": request.form["password"],
            "cpassword": request.form["cPassword"]}

    if user["password"] == user["cpassword"]:
        # creating a connection to database and initializing the cursor
        new_user = Users(firstName=user["fname"], lastName=user["lname"], email=user["email"], bio=user["bio"],
                         username=user["username"], password=user["password"])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"token": token_generate(new_user.username)}), 200

    else:
        return Response(
            response=json.dumps(
                {"message": "Password Incorrect. Try again!!"}),
            status=401,
            mimetype="application/json")


@app.route(version + '/user/<int:u_id>', methods=['GET'])
@token_required
def get_one_user(current_user, u_id):
    user = Users.query.filter_by(id=u_id).first()

    if not user:
        return jsonify({'success': False, 'message': 'No user found!'})

    user_data = {'u_id': user.id, 'firstName': user.firstName, 'lastName': user.lastName, 'username': user.username, 'bio': user.bio,
                 'email': user.email}
    return jsonify({'success': True, 'user': user_data, })


@app.route(version + '/current-user', methods=['GET'])
@token_required
def get_current_user(current_user):
    user = Users.query.filter_by(id=current_user.id).first()
    user_data = {}
    user_data['u_id'] = user.id
    user_data['firstName'] = user.firstName
    user_data['lastName'] = user.lastName
    user_data['email'] = user.email
    user_data['username'] = user.username
    user_data['bio'] = user.bio

    return jsonify({'user': user_data})

# Route to get all users


@app.route(version + '/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = Users.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['u_id'] = user.id
        user_data['firstName'] = user.firstName
        user_data['lastName'] = user.lastName
        user_data['email'] = user.email
        user_data['username'] = user.username
        user_data['bio'] = user.bio
        output.append(user_data)
    if not len(output):
        return Response(
            response=json.dumps({"message": "No Users Exists"}),
            status=401,
            mimetype="application/json"
        )
    return jsonify({'users': output})


# Route to search for a user
@app.route(version + '/search-user', methods=['GET'])
@token_required
def search_user(current_user):
    # getting the search query from the url
    search = request.args.get('search')
    # using try catch for sys error and check pass
    users = Users.query.filter(
        Users.username.like("%" + search + "%")).all()
    if not users:
        return jsonify({'message': "No Users Found"})
    output = []
    for user in users:
        user_data = {}
        user_data['u_id'] = user.id
        user_data['firstName'] = user.firstName
        user_data['lastName'] = user.lastName
        user_data['email'] = user.email
        user_data['username'] = user.username
        user_data['bio'] = user.bio
        output.append(user_data)
    if not len(output):
        return jsonify({'message': "No Users Found"})
    return jsonify({'users': output})
