from core import db, Booking, Player


def add_booking_query(spot_id, day, start_time, end_time, customer_id, user):
    booking = Booking(day=day,
                      start_time=start_time,
                      end_time=end_time,
                      spot_id=spot_id,
                      customer_id=customer_id)
    db.session.add(booking)
    target = Player.query.filter_by(user_id=user.id).first()
    lineup = Lineup(player_id=target.player_id,
                    booking_id=booking.booking_id)
    db.session.add(lineup)
    db.session.commit()
    return True
