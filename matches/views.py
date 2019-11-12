from . import match

from flask import request
from core import db, Match, Team, token_required


@match.route('/match', methods=['POST'])
@token_required
def create_match(current_user):
    data = request.get_json()
    home_team = Team(name=data['home_team_name'],
                     captain_id=current_user.id)
    db.session.add(home_team)

    away_team = Team(name=data['away_team_name'])
    db.session.add(away_team)

    db.session.flush()

    match = Match(date=data['date'],
                  duration=data['duration'],
                  creator_id=current_user.id,
                  home_team_id=home_team.team_id,
                  away_team_id=away_team.team_id)

    db.session.add(match)
    db.session.commit()

    return {'message': 'Match created!'}
