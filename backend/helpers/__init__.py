import datetime
import jwt
from functools import wraps
from flask import request, jsonify
from models.user_model import Users
from routes import app

def token_required(f):
    # wrapper function for the jwt authentication
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(
                id=data['u_id']).first()
        except:
            return jsonify({"message": "Token is Invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def token_generate(username):
    # this is to generate the jwt token
    u_id = Users.query.filter_by(username=username).first().id

    token = jwt.encode({'u_id': u_id, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
    return token
