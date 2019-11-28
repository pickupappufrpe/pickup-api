from flask import request

from core import db, Player, User, Person, PlayerInvite, token_required, Lineup
from . import player


@player.route('/players', methods=['GET'])
@token_required
def get_players(current_user):
    target = Player.query.join(User, Player.user_id == User.id).\
        join(Person, User.person_id == Person.id).\
        add_columns(Player.player_id, Person.name, Person.surname, Player.matches_count, Player.average_rating)

    output = []
    for p in target:
        player_data = {'name': p.name,
                       'id': p.player_id,
                       'surname': p.surname,
                       'matches_count': p.matches_count,
                       'average_rating': p.average_rating}
        output.append(player_data)

    return {'players': output}


@player.route('/players/invites', methods=['POST'])
@token_required
def invite_player(current_user):
    data = request.get_json()
    invite = PlayerInvite(player_id=data['player_id'],
                          booking_id=data['booking_id'])
    db.session.add(invite)
    db.session.flush()
    return {'message': 'Success!'}


@player.route('/players/invites/my', methods=['GET'])
@token_required
def get_my_invites(current_user):
    target = Player.query.filter_by(user_id=current_user.id).first()
    invites = PlayerInvite.query.filter_by(player_id=target.player_id)

    output = []

    for i in invites:
        invite_data = {'booking_id': i.booking_id,
                       'status': i.status,
                       'invite_id': i.playerinvite_id}
        output.append(invite_data)

    return {'bookings': output}


@player.route('/players/invites/accept', methods=['POST'])
@token_required
def accept_invite(current_user):
    data = request.get_json()
    invite = PlayerInvite.query.filter_by(invite_id=data['invite_id'])
    invite.status = True
    invite.answered = True
    db.session.add(invite)
    lineup = Lineup(player_id=data['player_id'],
                    booking_id=data['booking_id'])
    db.session.add(lineup)
    db.session.commit()
    return {'message': 'Success!'}
