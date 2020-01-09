from models import Player, PlayerInvite


def my_invites(user_id):
    player = Player.query.filter_by(user_id=user_id).first()
    invites = PlayerInvite.query.filter_by(guest_id=player.player_id)


'''
    # targets = SUPER_JOIN
    booking = Booking.query.filter_by(booking_id=i.booking_id).first()
    spot = Spot.query.filter_by(id=booking.spot_id).first()
    host_player = Player.query.filter_by(player_id=i.host_id).first()
    host_user = User.query.filter_by(id=host_player.user_id).first()
    host_person = Person.query.filter_by(id=host_user.person_id).first()  # TODO: refactor queries
'''