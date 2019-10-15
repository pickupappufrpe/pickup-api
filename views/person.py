from flask import request, Blueprint
from control import token_required

person_bp = Blueprint('person', __name__)
from core import db, User, Person


@person_bp.route('/person', methods=['POST'])
def create_person():
    data = request.get_json()
    result = Person(name=data['name'], surname=data['surname'])
    db.session.add(result)
    db.session.flush()
    new_person_id = str(result.id)
    db.session.commit()
    return {'message': 'New Person created!', "person_id": new_person_id}


@person_bp.route('/user/<user_id>/person', methods=['POST'])
def set_person(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    target = Person.query.filter_by(id=data['person_id']).first()
    user.person_id = target.id
    db.session.add(user)
    db.session.commit()
    return {'message': "Person has been set!"}


@person_bp.route('/user/<user_id>/person', methods=['GET'])
@token_required
def get_person(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()

    target = Person.query.filter_by(id=user.person_id).first()

    if not target:
        return {'message': "Person not found!"}

    return {'name': target.name, 'surname': target.surname}


@person_bp.route('/person', methods=['GET'])
@token_required
def get_all_people(current_user):
    people = Person.query.all()

    output = []

    for individual in people:
        individual_data = {'id': individual.id,
                           'name': individual.name,
                           'surname': individual.surname}

        output.append(individual)

    return {'people': output}
