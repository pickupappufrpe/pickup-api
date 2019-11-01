from . import address

from core import db, Address, State, City, token_required
from flask import request


@address.route('/address', methods=['POST'])
@token_required
def create_address(current_user):
    data = request.get_json()
    target = Address(street=data['street'],
                     number=data['number'],
                     neighborhood=data['neighborhood'],
                     cep=data['cep'])
    db.session.add(target)
    db.session.flush()
    new_address_id = str(target.id)
    db.session.commit()
    return {'message': 'New Address created!', "address_id": new_address_id}


@address.route('/state', methods=['POST'])
@token_required
def create_state(current_user):
    data = request.get_json()
    new_state = State(name=data['state_name'])
    db.session.add(new_state)
    db.session.flush()
    new_state_id = new_state.id
    db.session.commit()
    return {'message': 'New state created!', "new_state_id": str(new_state_id)}


@address.route('/city', methods=['POST'])
@token_required
def create_city(current_user):
    data = request.get_json()
    new_city = City(name=data['city_name'])
    db.session.add(new_city)
    db.session.flush()
    new_city_id = new_city.id
    db.session.commit()
    return {'message': 'New city created!', "new_city_id": str(new_city_id)}


@address.route('/city/<city_id>/state', methods=['POST'])
@token_required
def set_state(current_user, city_id):
    data = request.get_json()
    city = City.query.filter_by(id=city_id).first()
    state = State.query.filter_by(name=data['state_name']).first()
    city.state_id = state.id
    db.session.add(city)
    db.session.commit()
    return {'message': 'State has been set!'}


@address.route('/address/<address_id>/city', methods=['POST'])
@token_required
def set_city(current_user, address_id):
    data = request.get_json()
    target = Address.query.filter_by(id=address_id).first()
    city = City.query.filter_by(id=data['city_id']).first()
    target.city_id = city.id
    db.session.add(target)
    db.session.commit()
    return {'message': 'City has been set!'}


@address.route('/city/<city_id>', methods=['GET'])
@token_required
def get_city(current_user, city_id):
    city = City.query.filter_by(id=city_id).first()
    if not city:
        return {'message': 'No city found!'}
    return {'city_name': city.name, 'state_id': str(city.state_id)}


@address.route('/state/<state_id>', methods=['GET'])
@token_required
def get_state(current_user, state_id):
    state = State.query.filter_by(id=state_id).first()
    if not state:
        return {'message': 'No city found!'}
    return {'state_name': state.name}


@address.route('/city', methods=['GET'])
@token_required
def get_all_cities(current_user):
    cities = City.query.all()

    output = []

    for city in cities:
        city_data = {
                     'id': city.id,
                     'name': city.name,
                     'state_id': city.state_id
                     }

        output.append(city_data)

    return {'cities': output}


@address.route('/state', methods=['GET'])
@token_required
def get_all_states(current_user):
    states = State.query.all()

    output = []

    for state in states:
        state_data = {
                     'id': state.id,
                     'name': state.name
                     }

        output.append(state_data)

    return {'states': output}


@address.route('/state/<state_id>/city', methods=['GET'])
@token_required
def get_city_by_state(current_user, state_id):
    cities = City.query.filter_by(state_id=state_id)

    output = []

    for city in cities:
        city_data = {
                     'id': city.id,
                     'name': city.name,
                     }

        output.append(city_data)

    return {'cities': output}
