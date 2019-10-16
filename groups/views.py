from . import group

from flask import request
from core import Group, User, db, token_required


@group.route('/group', methods=['POST'])
@token_required
def create_group(current_user):
    data = request.get_json()
    user_group = Group(group_name=data['group_name'])
    db.session.add(user_group)
    db.session.commit()
    return {'message': "New User Group created!"}


@group.route('/group', methods=['GET'])
def get_all_groups(current_user):
    groups = Group.query.all()

    output = []

    for g in groups:
        group_data = {
                    'id': g.id,
                    'group_name': g.group_name
                    }
        output.append(group_data)

    return {'groups': output}


@group.route('/user/<user_id>/group', methods=['POST'])
def set_group(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    target = Group.query.filter_by(group_name=data['group']).first()
    user.group_id = target.id
    db.session.add(user)
    db.session.commit()
    return {'message': 'User Group has been set!'}