from . import booking

from flask import request
from core import token_required, Booking, Spot
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


@booking.route('/spot/<spot_id>/booking', methods=['GET'])
@token_required
def get_spot_bookings(current_user, spot_id):
    bookings = Booking.query.filter_by(spot_id=spot_id)

    output = []

    for b in bookings:
        bookings_data = {
            'day': b.day,
            'spot_id': b.spot_id,
            'start_time': str(b.start_time),
            'end_time': str(b.end_time),
        }

        output.append(bookings_data)

    return {'bookings': output}


@booking.route('/booking/my', methods=['GET'])
@token_required
def get_my_bookings(current_user):
    bookings = Booking.query.join(Spot, Spot.id == Booking.spot_id). \
            add_columns(Spot.name, Booking.day, Booking.start_time, Booking.end_time). \
            filter(Booking.customer_id == current_user.id)
    output = []
    for b in bookings:
        bookings_data = {
            'day': b.day,
            'spot_name': b.name,
            'start_time': str(b.start_time),
            'end_time': str(b.end_time),
        }

        output.append(bookings_data)

    return {'bookings': output}


@booking.route('/booking/my/owner', methods=['GET'])
@token_required
def get_my_spots_bookings(current_user): # TODO: refactor, create control functions to reuse in get_spot_bookings
    output = []
    my_spots = Spot.query.filter_by(owner_id=current_user.id)
    for i in my_spots:
        bookings = Booking.query.filter_by(spot_id=i.id)

        spot_bookings = []

        for b in bookings:
            bookings_data = {
                'day': b.day,
                'spot_id': b.spot_id,
                'start_time': str(b.start_time),
                'end_time': str(b.end_time)
            }

            spot_bookings.append(bookings_data)
    output.append(spot_bookings)
    return {'bookings': output}
