import datetime

import jwt
from flask import request, make_response
from werkzeug.security import check_password_hash

from controllers import token_required
from core import app
from models import db, User
from . import user
from .controls import signup_query, get_user_by_id_query


@user.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    search = User.query.filter_by(username=data['username']).first()
    if search is None:
        new_user_id = signup_query(data['username'],
                                   data['password'],
                                   data['name'],
                                   data['surname'],
                                   data['group_id'])

        return {'message': 'New user created!', "new_user_id": new_user_id}
    else:
        return {'message': 'User already exist!'}


@user.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    asked_group = request.args.get("user_group")
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    result = User.query.filter_by(username=auth.username, group_id= asked_group).first()

    if not result:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # if user.group_id != int(asked_group):
    #     return {'message': "Wrong user group!"}

    if check_password_hash(result.password, auth.password):
        token = jwt.encode({
                            'id': str(result.id),
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                            },
                           app.config['SECRET_KEY'])

        return {'token': token.decode('UTF-8')}

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@user.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    target = get_user_by_id_query(user_id)
    print(type(target))

    return {'username': target.username,
            'name': target.name,
            'surname': target.surname,
            'group_id': target.group_id
            }


@user.route('/user/username/<username>', methods=['GET'])
@token_required
def get_user_by_username(username):
    username = str(username)
    target = User.query.filter_by(username=username).first()

    if not target:
        return {'message': 'No user found!'}

    return {'id': target.id,
            'username': target.username,
            'group_id': target.group_id,
            'person_id': target.person_id,
            'contact_id': target.contact_id
            }


@user.route('/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    target = User.query.filter_by(id=user_id).first()

    if not target:
        return {'message': 'No user found!'}

    db.session.delete(target)
    db.session.commit()

    return {'message': 'The user has been deleted!'}
