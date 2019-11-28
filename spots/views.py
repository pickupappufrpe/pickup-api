from flask import request

from core import Spot, token_required, SpotRating, db
from . import spot
from .controls import create_address_query, create_contact_query, create_spot_query, render_spot_group


@spot.route('/spot', methods=['POST'])
@token_required
def create_spot(current_user):
    data = request.get_json()
    address_id = create_address_query(data['city_id'],
                                      data['street'],
                                      data['cep'],
                                      data['number'],
                                      data['neighborhood'])

    contact_id = create_contact_query(data['email'],
                                      data['phone'])

    spot_id = create_spot_query(data['spot_name'],
                                data['price'],
                                data['ground_id'],
                                current_user.id,
                                address_id,
                                contact_id)
    return {'message': 'New Spot created!', "spot_id": spot_id}


@spot.route('/spot/my', methods=['GET'])
@token_required
def get_my_spots(current_user):
    spots = Spot.query.filter_by(owner_id=current_user.id)
    return render_spot_group(spots)


@spot.route('/spot', methods=['GET'])
@token_required
def get_all_spots(current_user):
    spots = Spot.query.all()
    return render_spot_group(spots)

@spot.route('/spot/<spot_id>', methods=['GET'])
@token_required
def get_all_spots(current_user,spot_id):
    spot = Spot.query.filter_by(id=spot_id)
    return render_spot(spot)


@spot.route('/spot/rate', methods=['POST'])
@token_required
def rate_spot(current_user):
    data = request.get_json()
    rating = SpotRating(rating=data['rating'],
                        spot_id=data['spot_id'],
                        evaluator_id=current_user.id)
    db.session.add(rating)
    db.session.commit()
    return {'message': 'Success!'}
