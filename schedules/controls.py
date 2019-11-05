from core import db, Schedule


def add_schedule_query(spot_id, week_day, opening_time, closing_time):
    schedule = Schedule(spot_id=spot_id,
                        week_day=week_day,
                        opening_time=opening_time,
                        closing_time=closing_time)
    db.session.add(schedule)
    db.session.commit()
    return True
