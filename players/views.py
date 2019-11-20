from flask import request

from core import db, Player, User, Person, PlayerInvite, token_required
from . import player


@player.route('/players', methods=['GET'])
@token_required
def get_players(current_user):
    target = Player.query.join(User, Player.user_id == User.id).\
        join(Person, User.person_id == Person.id).\
        add_columns(Person.name, Person.surname, Player.matches_count, Player.average_rating)

    output = []
    for p in target:
        player_data = {'name': p.name,
                       'surname': p.surname,
                       'matches_count': p.matches_count,
                       'average_rating': p.average_rating}
        output.append(player_data)

    return {'players': output}


@player.route('players/invite', methods=['post'])
@token_required
def invite_player(current_user):
    data = request.get_json()
    invite = PlayerInvite(player_id=data['player_id'],
                          booking_id=data['booking_id'])
    db.session.add(invite)
    db.session.flush()
    return {'message': 'Success!'}
