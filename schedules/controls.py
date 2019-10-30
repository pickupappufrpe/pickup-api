from core import db, Schedule, Spot, User


def add_schedule_query(spot_id, week_day, opening_time, closing_time):
    schedule = Schedule(spot_id=spot_id,
                        week_day=week_day,
                        opening_time=opening_time,
                        closing_time=closing_time)
    db.session.add(schedule)
    db.session.commit()
    return True


def get_spot_schedules_query(spot_id):
    schedules = Schedule.query.filter_by(spot_id=spot_id)

    output = []

    for s in schedules:
        schedules_data = {
            'schedule_id': s.schedule_id,
            'spot_id': s.spot_id,
            'week_day': s.week_day,
            'opening_time': s.opening_time,
            'closing_time': s.closing_time
        }

        output.append(schedules_data)

    return {'schedules': output}