from core import db, User, Person
from werkzeug.security import generate_password_hash


def signup_query(username, password, name, surname, group_id):
    person = Person(name=name,
                    surname=surname)
    db.session.add(person)
    db.session.flush()
    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username,
                password=hashed_password,
                person_id=person.id,
                group_id=group_id)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return user.id


def get_user_by_id_query(user_id):
    target = User.query.join(Person, Person.id == User.person_id). \
             add_columns(Person.name, Person.surname, User.username, User.group_id). \
             filter(User.id == user_id).filter(Person.id == User.person_id).first()
    # TODO: incluir contato na query
    if not target:
        return {'message': 'Sorry!'}
    return target
