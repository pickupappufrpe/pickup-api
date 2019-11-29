from . import booking

from flask import request
from core import token_required, Booking, Spot, Lineup, Player, Person, User
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
            add_columns(Booking.spot_id,Booking.booking_id, Spot.name, Booking.day, Booking.start_time, Booking.end_time). \
            filter(Booking.customer_id == current_user.id)
    output = []
    for b in bookings:
        bookings_data = {
            'day': b.day,
            'id': b.booking_id,
            'spot_id': b.spot_id,
            'spot_name': b.name,
            'start_time': str(b.start_time),
            'end_time': str(b.end_time),
        }

        output.append(bookings_data)

    return {'bookings': output}


@booking.route('/booking/my/invited', methods=['GET'])
@token_required
def get_my_invited_bookings(current_user):
    player = Player.query.filter_by(user_id=current_user.id).first()
    lineups = Lineup.query.filter_by(player_id=player.player_id)
    output = []
    for l in lineups:
        target = Booking.query.filter_by(booking_id=l.booking_id).first()
        spot = Spot.query.filter_by(id=target.spot_id).first()
        output.append({
                'day': booking.day,
                'spot_id': booking.spot_id,
                'spot_name': spot.name,
                'start_time': str(booking.start_time),
                'end_time': str(booking.end_time)})
    return {'bookings': output}


@booking.route('/booking/my/owner', methods=['GET'])
@token_required
def get_my_spots_bookings(current_user): # TODO: refactor, create control functions to reuse in get_spot_bookings
    output = []
    my_spots = Spot.query.filter_by(owner_id=current_user.id)
    for i in my_spots:
        bookings = Booking.query.filter_by(spot_id=i.id)
        # spot_bookings = []
        for b in bookings:
            bookings_data = {
                'day': b.day,
                'spot_id': b.spot_id,
                'spot_name':i.name,
                'start_time': str(b.start_time),
                'end_time': str(b.end_time)
            }
            # spot_bookings.append(bookings_data)
            output.append(bookings_data)
    return {'bookings': output}


@booking.route('/booking/<booking_id>/players', methods=['GET'])
@token_required
def get_booking_players(current_user, booking_id):
    lineups = Lineup.query.filter_by(booking_id=booking_id)
    output = []
    for l in lineups:
        player = Player.query.filter_by(player_id=l.player_id).first()
        target = Player.query.join(User, player.user_id == User.id). \
            join(Person, User.person_id == Person.id). \
            add_columns(Person.name, Person.surname, Player.matches_count, Player.average_rating).first()

        player_data = {'name': target.name,
                       'surname': target.surname,
                       'matches_count': target.matches_count,
                       'average_rating': target.average_rating}
        output.append(player_data)

        return {'players': output}
