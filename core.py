from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
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


@app.route('/')
def hello_world():
    return 'Hello, World!'


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


from users import user as user_bp
app.register_blueprint(user_bp)

from people import person as person_bp
app.register_blueprint(person_bp)

from contacts import contact as contact_bp
app.register_blueprint(contact_bp)

from groups import group as group_bp
app.register_blueprint(group_bp)


@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    # data = request.get_json()
    # asked_group = data['user_group']
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    result = User.query.filter_by(username=auth.username).first()

    if not result:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # if user.group_id != int(asked_group):
    #     return {'message': "Wrong user group!"}

    if check_password_hash(result.password, auth.password):
        token = jwt.encode({
                            'id': str(result.id),
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                            },
                           app.config['SECRET_KEY'])

        return {'token': token.decode('UTF-8')}

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


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


@app.route('/spot/<id>', methods=['GET'])
@token_required
def get_spot_by_id(current_user, id):
    spot = Spot.query.filter_by(id=id).first()

    if not spot:
        return {'message': 'Spot not found!'}

    return {'id': spot.id,
            'name': spot.name,
            'owner_id': spot.owner_id,
            'contact_id': spot.contact_id
            }


@app.route('/spot/my', methods=['GET'])
@token_required
def get_my_spots(current_user):
    spots = Spot.query.filter_by(owner_id=current_user.id)

    output = []

    for spot in spots:
        spot_data = {'id': spot.id,
                     'name': spot.name,
                     'owner_id': spot.owner_id,
                     'contact_id': spot.contact_id
                     }

        output.append(spot_data)

    return {'spots': output}


@app.route('/spot', methods=['GET'])
@token_required
def get_all_spots(current_user):
    spots = Spot.query.all()

    output = []

    for spot in spots:
        spot_data = {'id': spot.id,
                     'name': spot.name,
                     'owner_id': spot.owner_id,
                     'contact_id': spot.contact_id
                     }

        output.append(spot_data)

    return {'spots': output}


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
