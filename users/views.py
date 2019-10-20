from . import user

from flask import request
from werkzeug.security import generate_password_hash
# from control import token_required
from core import User, Person, db, token_required


@user.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    search = User.query.filter_by(username=data['username']).first()
    if search is None:
        new_person = Person(name = data['name'], surname = data['surname'])
        db.session.add(new_person)
        db.session.flush()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password=hashed_password, person_id = new_person.id, group_id = data['group'])
        db.session.add(new_user)
        db.session.flush()
        new_id = str(new_user.id)
        db.session.commit()
        return {'message': 'New user created!', "new_user_id": new_id}
    else:
        return {'message': 'User already exist!'}


@user.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):

    target = User.query.filter_by(id=user_id).first()

    if not target:
        return {'message': 'No user found! BLASH'}

    user_data = {
                 'id': target.id,
                 'username': target.username,
                 'group_id': target.group_id,
                 'person_id': target.person_id,
                 'contact_id': target.contact_id
                 }
    return {'user': user_data}


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


@user.route('/user/full/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    target = db.session.query(
                              User.username,
                              Person.name,
                              Person.surname
                              ).join(User).join(Person, Person.id == User.person_id).first()

    if not target:
        return {'message': 'Sorry!'}

    return {'username': target.username,
            'name': target.name,
            'surname': target.surname}
