from . import booking

from flask import request
from core import token_required
from .controls import add_booking_query


@booking.route('/booking', methods=['POST'])
@token_required
def add_booking(current_user):
    data = request.get_json()
    if add_booking_query(data['day'],
                         data['start_time'],
                         data['end_time'],
                         data['spot_id'],
                         current_user.id):
        return {'message': 'Booking saved!'}
