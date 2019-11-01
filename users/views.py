from . import user

from flask import request
from core import db, User, token_required
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


@user.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()

    output = []

    for individual in users:
        user_data = {
            'id': individual.id,
            'username': individual.username
        }

        output.append(user_data)

    return {'users': output}


@user.route('/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    target = User.query.filter_by(id=user_id).first()

    if not target:
        return {'message': 'No user found!'}

    db.session.delete(target)
    db.session.commit()

    return {'message': 'The user has been deleted!'}


@user.route('/players', methods=['GET'])
@token_required
def get_players(current_user):
    target = db.engine.execute('SELECT "user".username, person.name, person.surname '
                               'FROM "user" '
                               'INNER JOIN person '
                               'ON "user".person_id = person.id '
                               'WHERE "user".group_id = 1')
    output = []
    for i in target:
        player_data = {'username': i[0],
                       'name': i[1],
                       'surname': i[2]}

        output.append(player_data)

    return {'players': output}
