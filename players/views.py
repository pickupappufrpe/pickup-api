from . import player

from core import Player, User, Person, token_required


@player.route('/players', methods=['GET'])
@token_required
def get_players(current_user):
    target = Player.query.join(User, Player.user_id == User.id).\
        join(Person, User.person_id == Person.id).\
        add_columns(Person.name, Person.surname, Player.matches_count, Player.average_rating)

    output = []
    for p in target:
        player_data = {'name': target.name,
                       'surname': target.surname,
                       'matches_count': target.matches_count,
                       'average_rating': target.average_rating}
        output.append(player_data)

    return {'players': output}
