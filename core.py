from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import datetime
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    spots = db.relationship("Spot")


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    users = db.relationship("User", uselist=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    phone = db.Column(db.String(11))
    users = db.relationship("User")
    spots = db.relationship("Spot")


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20))
    users = db.relationship("User", uselist=False)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    cep = db.Column(db.String(8))
    number = db.Column(db.Integer)
    neighborhood = db.Column(db.String(30))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    spots = db.relationship("Spot", uselist=False)


class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    cities = db.relationship("City")


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    addresses = db.relationship("Address")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'message': 'Token is missing!'}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            if 'id' in data:
                current_user = User.query.filter_by(id=data['id']).first()
                return f(current_user, *args, **kwargs)
        except Exception as e:
            return {'message': str(e.with_traceback())}, 401

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    search = User.query.filter_by(username=data['username']).first()
    if search is None:
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.flush()
        new_id = str(new_user.id)
        db.session.commit()
        return {'message': 'New user created!', "new_user_id": new_id}
    else:
        return {'message': 'User already exist!'}

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username

        output.append(user_data)

    return {'users' : output}


@app.route('/user/<id>', methods=['GET'])
@token_required
def get_one_user(current_user, id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return {'message' : 'No user found!'}

    user_data = {}
    user_data['id'] = user.id
    user_data['username'] = user.username
    user_data['group_id'] = user.group_id
    user_data['person_id'] = user.person_id
    user_data['contact_id'] = user.contact_id
    return {'user': user_data}

@app.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return {'message': 'No user found!'}

    db.session.delete(user)
    db.session.commit()

    return {'message': 'The user has been deleted!'}

@app.route('/login')
@token_required
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : str(user.id), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return {'token' : token.decode('UTF-8')}

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/person', methods=['POST'])
@token_required
def create_person():
    data = request.get_json()
    person = Person(name=data['name'], surname=data['surname'])
    db.session.add(person)
    db.session.flush()
    new_person_id = str(person.id)
    db.session.commit()
    return {'message': 'New Person created!', "person_id": new_person_id}


@app.route('/user/<id>/person', methods=['POST'])
@token_required
def set_person(id):
    data = request.get_json()
    user = User.query.filter_by(id=id).first()
    person = Person.query.filter_by(id=data['person_id']).first()
    user.person_id = person.id
    db.session.add(user)
    db.session.commit()
    return {'message': "Person has been set!"}


@app.route('/user/<id>/person', methods=['GET'])
@token_required
def get_person(current_user, id):
    user = User.query.filter_by(id=id).first()

    person = Person.query.filter_by(id=user.person_id).first()

    if not person:
        return {'message': "Person not found!"}

    return {'name': person.name, 'surname': person.surname}


@app.route('/person', methods=['GET'])
@token_required
def get_all_persons(current_user):
    persons = Person.query.all()

    output = []

    for person in persons:
        person_data = {'id': person.id,
                       'name': person.name,
                       'surname': person.surname}

        output.append(person_data)

    return {'persons': output}


@app.route('/contact', methods=['POST'])
@token_required
def create_contact():
    data = request.get_json()
    contact = Contact(email=data['email'], phone=data['phone'])
    db.session.add(contact)
    db.session.flush()
    new_contact_id = str(contact.id)
    db.session.commit()
    return {'message': 'New Contact created!', "contact_id": new_contact_id}


@app.route('/user/<id>/contact', methods=['POST'])
@token_required
def set_contact(id):
    data = request.get_json()
    user = User.query.filter_by(id=id).first()
    contact = Contact.query.filter_by(id=data['contact_id']).first()
    user.contact_id = contact.id
    db.session.add(user)
    db.session.commit()
    return {'message': "Contact has been set!"}


@app.route('/user/<id>/contact', methods=['GET'])
@token_required
def get_contact(current_user, id):
    user = User.query.filter_by(id=id).first()
    contact = Contact.query.filter_by(id=user.contact_id).first()

    if not contact:
        return {'message': "Contact not found!"}

    return {'email': contact.email, 'phone': contact.phone}


@app.route('/group', methods=['POST'])
@token_required
def create_group():  # TODO: ask current user
    data = request.get_json()
    user_group = Group(group_name=data['group_name'])
    db.session.add(user_group)
    db.session.commit()
    # TODO: return new group id
    return {'message': "New User Group created!"}


@app.route('/group', methods=['GET'])
@token_required
def get_all_groups(current_user):
    groups = Group.query.all()

    output = []

    for group in groups:
        group_data = {'id': group.id, 'group_name': group.group_name}
        output.append(group_data)

    return {'groups': output}


@app.route('/user/<id>/group', methods=['POST'])
@token_required
def set_group(id):
    data = request.get_json()
    user = User.query.filter_by(id=id).first()
    group = Group.query.filter_by(group_name=data['group']).first()
    user.group_id = group.id
    db.session.add(user)
    db.session.commit()
    return {'message': 'User Group has been set!'}


@app.route('/address', methods=['POST'])
@token_required
def create_address(current_user):
    data = request.get_json()
    address = Address(street=data['street'],
                      number=data['number'],
                      neighborhood=data['neighborhood'],
                      cep=data['cep']
                      )
    db.session.add(address)
    db.session.flush()
    new_address_id = str(address.id)
    db.session.commit()
    return {'message': 'New Address created!', "address_id": new_address_id}


@app.route('/spot/<id>/address', methods=['POST'])
@token_required
def set_address(current_user, id):
    data = request.get_json()
    spot = Spot.query.filter_by(id=id).first()
    address = Address.query.filter_by(id=data['address_id']).first()
    spot.address_id = address.id
    db.session.add(spot)
    db.session.commit()
    return {'message': "Address has been set!"}


@app.route('/spot/<id>/address', methods=['GET'])
@token_required
def get_address(current_user, id):
    spot = Spot.query.filter_by(id=id).first()

    if not spot:
        return {'message': "Spot not found!"}

    address = Address.query.filter_by(id=str(spot.address_id)).first()

    if not address:
        return {'message': "Address not found!"}

    return {'street': str(address.street),
            'number': str(address.number),
            'neighborhood': str(address.neighborhood),
            'city': str(address.city_id),
            'cep': address.cep
            }


@app.route('/spot', methods=['POST'])
@token_required
def create_spot(current_user):
    data = request.get_json()
    spot = Spot(owner_id=current_user.id,
                name=data['spot_name'])
    db.session.add(spot)
    db.session.flush()
    new_spot_id = str(spot.id)
    db.session.commit()
    return {'message': 'New Spot created!', "spot_id": new_spot_id}


@app.route('/spot/<id>/contact', methods=['POST'])
@token_required
def set_spot_contact(current_user, id):
    data = request.get_json()
    spot = Spot.query.filter_by(id=id).first()
    contact = Contact.query.filter_by(id=data['contact_id']).first()
    spot.contact_id = contact.id
    db.session.add(spot)
    db.session.commit()
    return {'message': 'Contact has been set!'}


@app.route('/state', methods=['POST'])
@token_required
def create_state(current_user):
    data = request.get_json()
    new_state = State(name=data['state_name'])
    db.session.add(new_state)
    db.session.flush()
    new_state_id = new_state.id
    db.session.commit()
    return {'message': 'New state created!', "new_state_id": str(new_state_id)}


@app.route('/city', methods=['POST'])
@token_required
def create_city(current_user):
    data = request.get_json()
    new_city = City(name=data['city_name'])
    db.session.add(new_city)
    db.session.flush()
    new_city_id = new_city.id
    db.session.commit()
    return {'message': 'New city created!', "new_city_id": str(new_city_id)}


@app.route('/city/<id>/state', methods=['POST'])
@token_required
def set_state(current_user, id):
    data = request.get_json()
    city = City.query.filter_by(id=id).first()
    state = State.query.filter_by(name=data['state_name']).first()
    city.state_id = state.id
    db.session.add(city)
    db.session.commit()
    return {'message': 'State has been set!'}


@app.route('/address/<id>/city', methods=['POST'])
@token_required
def set_city(current_user, id):
    data = request.get_json()
    address = Address.query.filter_by(id=id).first()
    city = City.query.filter_by(id=data['city_id']).first()
    address.city_id = city.id
    db.session.add(address)
    db.session.commit()
    return {'message': 'City has been set!'}


@app.route('/city/<id>', methods=['GET'])
@token_required
def get_city(current_user, id):
    city = City.query.filter_by(id=id).first()
    if not city:
        return {'message': 'No city found!'}
    return {'city_name': city.name, 'state_id': str(city.state_id)}


@app.route('/state/<id>', methods=['GET'])
@token_required
def get_state(current_user, id):
    state = State.query.filter_by(id=id).first()
    if not state:
        return {'message': 'No city found!'}
    return {'state_name': state.name}


@app.route('/city', methods=['GET'])
@token_required
def get_all_cities(current_user):
    cities = City.query.all()

    output = []

    for city in cities:
        city_data = {
                     'id': city.id,
                     'name': city.name,
                     'state_id': city.state_id
                     }

        output.append(city_data)

    return {'cities': output}


@app.route('/state', methods=['GET'])
@token_required
def get_all_states(current_user):
    states = State.query.all()

    output = []

    for state in states:
        state_data = {
                     'id': state.id,
                     'name': state.name
                     }

        output.append(state_data)

    return {'states': output}


if __name__ == '__main__':
    app.run()
