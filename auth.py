from flask import request
import jwt
from users import fetch_users_by_criteria
from login import secret_key


def get_current_user():
    token = request.cookies.get('token')
    if token:
        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            userdata = fetch_users_by_criteria(username=data.get('username'))
            return userdata
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None


def get_user_variables():
    current_user = get_current_user()
    if current_user:
        user_info = current_user[0]
        user_id = user_info['id']
        telephone = user_info['telephone']
        username = user_info['username']
        agence = user_info['agence']
        role = user_info['role']
        privileges = user_info['privileges']
        return user_id, telephone, username, agence, role, privileges
    else:
        return None, None, None, None, None, None

