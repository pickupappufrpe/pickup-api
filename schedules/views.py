from . import schedule

from flask import request
from core import token_required, Schedule
from .controls import add_schedule_query


@schedule.route('/schedule', methods=['POST'])
@token_required
def add_schedule(current_user):
    data = request.get_json()
    if add_schedule_query(data['spot_id'],
                          data['week_day'],
                          data['opening_time'],
                          data['closing_time']):
        return {'message': 'Schedule added!'}


@schedule.route('/schedule', methods=['GET'])
@token_required
def get_all_schedules(current_user):
    schedules = Schedule.query.all()

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


@schedule.route('/spot/schedule/<spot_id>', methods=['GET'])
@token_required
def get_spot_schedules(current_user, spot_id):
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
