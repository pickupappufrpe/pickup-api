from controllers import token_required
from models import State, City
from . import address


@address.route('/state', methods=['GET'])
@token_required
def get_all_states(current_user):
    states = State.query.all()
    output = []
    for state in states:
        state_data = {'id': state.id,
                      'name': state.name}
        output.append(state_data)
    return {'states': output}


@address.route('/state/<state_id>/city', methods=['GET'])
@token_required
def get_city_by_state(current_user, state_id):
    cities = City.query.filter_by(state_id=state_id)
    output = []
    for city in cities:
        city_data = {'id': city.id,
                     'name': city.name}
        output.append(city_data)
    return {'cities': output}
