from . import booking

from flask import request
from core import token_required, Booking, User
from .controls import add_booking_query


@booking.route('/booking', methods=['POST'])
@token_required
def add_booking(current_user):
    data = request.get_json()
    if add_booking_query(data['spot_id'],
                         data['day'],
                         data['start_time'],
                         data['end_time'],
                         current_user.id):
        return {'message': 'Booking saved!'}


@booking.route('/spot/booking', methods=['GET'])
@token_required
def get_all_bookings(current_user):
    bookings = Booking.query.all()

    output = []

    for b in bookings:
        bookings_data = {
            'day': b.day,
            'spot_id': b.spot_id,
            'start_time': b.start_time,
            'end_time': b.end_time,
        }

        output.append(bookings_data)

    return {'bookings': output}


@booking.route('/spot/<spot_id>/booking', methods=['GET'])
@token_required
def get_spot_bookings(current_user, spot_id):
    bookings = Booking.query.filter_by(spot_id=spot_id)

    output = []

    for b in bookings:
        bookings_data = {
            'day': b.day,
            'spot_id': b.spot_id,
            'start_time': b.start_time,
            'end_time': b.end_time,
        }

        output.append(bookings_data)

    return {'bookings': output}
