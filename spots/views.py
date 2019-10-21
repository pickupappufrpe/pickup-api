from . import spot

from core import db, Spot, Address, City, Contact, token_required, State
from flask import request


@spot.route('/spot/<spot_id>/address', methods=['POST'])
@token_required
def set_address(current_user, spot_id):
    data = request.get_json()
    target = Spot.query.filter_by(id=spot_id).first()
    address = Address.query.filter_by(id=data['address_id']).first()
    target.address_id = address.id
    db.session.add(target)
    db.session.commit()
    return {'message': "Address has been set!"}


@spot.route('/spot/<spot_id>/address', methods=['GET'])  # TODO: transferir para o pacote 'addresses'
@token_required
def get_address(current_user, spot_id):
    target = Spot.query.filter_by(id=spot_id).first()

    if not target:
        return {'message': "Spot not found!"}

    address = Address.query.filter_by(id=str(target.address_id)).first()

    if not address:
        return {'message': "Address not found!"}

    city = City.query.filter_by(id=address.city_id).first()
    state = State.query.filter_by(id=city.state_id).first()

    return {
            'street': address.street,
            'number': address.number,
            'neighborhood': address.neighborhood,
            'city': city.name,
            'state': state.name,
            'cep': address.cep
            }


@spot.route('/spot', methods=['POST'])
@token_required
def create_spot(current_user):
    data = request.get_json()
    city = City.query.filter_by(name=data['cidade']).first()
    state = State.query.filter_by(name=data['estado']).first()
    new_address = Address(street = data['street'],
                          cep = data['cep'],
                          number = data['numero'],
                          neighborhood = data['bairro'],
                          city_id = city.id,
                          state_id = state.id
                          )
    db.session.add(new_address)
    db.session.flush()
    new_contact = Contact(email = data['email'], phone = data['telefone'])
    new_spot = Spot(owner_id=current_user.id,
                    name=data['spot_name'],
                    address_id = new_address.id,
                    contact_id = new_contact.id
                    )
    db.session.add(new_spot)
    db.session.flush()
    new_spot_id = str(new_spot.id)
    db.session.commit()
    return {'message': 'New Spot created!', "spot_id": new_spot_id}


@spot.route('/spot/<spot_id>/contact', methods=['POST'])
@token_required
def set_spot_contact(current_user, spot_id):
    data = request.get_json()
    target = Spot.query.filter_by(id=spot_id).first()
    contact = Contact.query.filter_by(id=data['contact_id']).first()
    target.contact_id = contact.id
    db.session.add(target)
    db.session.commit()
    return {'message': 'Contact has been set!'}


@spot.route('/spot/<spot_id>', methods=['GET'])
@token_required
def get_spot_by_id(current_user, spot_id):
    target = Spot.query.filter_by(id=id).first()

    if not target:
        return {'message': 'Spot not found!'}

    return {'id': target.id,
            'name': target.name,
            'owner_id': target.owner_id,
            'contact_id': target.contact_id
            }


@spot.route('/spot/my', methods=['GET'])
@token_required
def get_my_spots(current_user):
    spots = Spot.query.filter_by(owner_id=current_user.id)

    output = []

    for s in spots:
        spot_data = {'id': s.id,
                     'name': s.name,
                     'owner_id': s.owner_id,
                     'contact_id': s.contact_id
                     }

        output.append(spot_data)

    return {'spots': output}


@spot.route('/spot', methods=['GET'])
@token_required
def get_all_spots(current_user):
    spots = Spot.query.all()

    output = []

    for s in spots:
        spot_data = {'id': s.id,
                     'name': s.name,
                     'owner_id': s.owner_id,
                     'contact_id': s.contact_id
                     }

        output.append(spot_data)

    return {'spots': output}