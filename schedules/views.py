from . import schedule

from flask import request
from core import token_required
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
