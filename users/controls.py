from models import db, User, Person, Player, Referee
from werkzeug.security import generate_password_hash


def create_person_query(name, surname):
    person = Person(name=name,
                    surname=surname)
    db.session.add(person)
    db.session.flush()
    return person.id


def create_user_query(username, password, person_id, group_id):
    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username,
                password=hashed_password,
                person_id=person_id,
                group_id=group_id)
    db.session.add(user)
    db.session.flush()
    return user.id


def create_player_query(user_id):
    player = Player(user_id=user_id)
    db.session.add(player)
    return True


def create_referee_query(user_id):
    referee = Referee(user_id=user_id)
    db.session.add(referee)
    return True


def signup_query(username, password, name, surname, group_id):
    person_id = create_person_query(name, surname)
    user_id = create_user_query(username, password, person_id, group_id)
    if group_id == "1":
        create_player_query(user_id)
    if group_id == "3":
        create_referee_query(user_id)
    db.session.commit()
    return user_id


def get_user_by_id_query(user_id):
    target = User.query.join(Person, Person.id == User.person_id). \
             add_columns(Person.name, Person.surname, User.username, User.group_id). \
             filter(User.id == user_id).filter(Person.id == User.person_id).first()
    # TODO: incluir contato na query
    if not target:
        return {'message': 'Sorry!'}
    print(type(target))
    return target


def get_players_query():
    target = User.query.join(Person, User.person_id == Person.id).\
             add_columns(User.username, Person.name, Person.surname).\
             filter(User.group_id == "1")
    return target
