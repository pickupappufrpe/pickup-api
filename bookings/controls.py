from core import db, Booking


def add_booking_query(spot_id, day, start_time, end_time, customer_id):
    booking = Booking(day=day,
                      start_time=start_time,
                      end_time=end_time,
                      spot_id=spot_id,
                      customer_id=customer_id)
    db.session.add(booking)
    db.session.commit()
    return True
