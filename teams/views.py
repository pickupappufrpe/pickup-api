from flask import request

from controllers import token_required
from models import db, User, Person, Team
from . import team


@team.route('/team', methods=['POST'])
@token_required
def create_team(current_user):
    data = request.get_json()
    new_team = Team(name=data['team_name'],
                    captain_id=current_user.id)
    db.session.add(new_team)
    db.session.flush()
    db.session.commit()
    return {'New team id': new_team.team_id}


@team.route('/team', methods=['GET'])
@token_required
def get_teams(current_user):
    teams = Team.query.all()
    output = []
    for t in teams:
        team_data = {'id': t.team_id,
                     'name': t.name}
        output.append(team_data)
    return {'teams': output}


@team.route('/team/<team_id>/lineup', methods=['POST'])
@token_required
def add_player_to_team(current_user, team_id):
    data = request.get_json()
    target = Team.query.filter_by(team_id=team_id).first()
    player = User.query.filter_by(id=data['user_id']).first()
    target.players.append(player)
    db.session.commit()
    return {'message': 'Success!'}


@team.route('/team/<team_id>/lineup', methods=['GET'])
@token_required
def get_players_from_team(current_user, team_id):
    target = Team.query.filter_by(team_id=team_id).first()
    output = []
    for player in target.players:
        person = Person.query.filter_by(id=player.id).first()
        player_data = {'name': person.name,
                       'surname': person.surname}
        output.append(player_data)
    return {'players': output}
