from flask import Flask, request, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import jwt
from functools import wraps
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.environ.get('DEBUG')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    spots = db.relationship("Spot")
    photos = db.relationship("Photo")
    players = db.relationship("Player", uselist=False)
    bookings = db.relationship("Booking")
    matches = db.relationship("Match")
    reporteds = db.relationship("Report", foreing_keys='Report.reported_id')
    reporters = db.relationship("Report", foreing_keys='Report.reporter_id')


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
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    spots = db.relationship("Spot", uselist=False)


class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Integer)
    average_rating = db.Column(db.Float)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    ground_id = db.Column(db.Integer, db.ForeignKey('ground.ground_id'))
    photos = db.relationship("Photo")
    schedules = db.relationship("Schedule")
    bookings = db.relationship("Booking")
    ratings = db.relationship("SpotRating")


class Ground(db.Model):
    ground_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    spots = db.relationship("Spot", uselist=False)


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    cities = db.relationship("City")


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    addresses = db.relationship("Address")


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'))
    image = db.Column(db.String(10485760))


class Schedule(db.Model):
    schedule_id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'))
    week_day = db.Column(db.Integer)
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)


class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    captain_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lineups = db.relationship("Lineup")


class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'))
    average_rating = db.Column(db.Float)
    matches_played = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    ratings = db.relationship("PlayerRating")
    lineups = db.relationship("Lineup")


class Position(db.Model):
    position_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    players = db.relationship("Player", uselist=False)


class SpotRating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'))
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class PlayerRating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reports = db.relationship("Report")
    lineups = db.relationship("Lineup")


class Lineup(db.Model):
    lineup_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    match_id = db.Column(db.Integer, db.ForeignKey('match.match_id'))


class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    scoresheet_id = db.Column(db.Integer, db.ForeignKey('scoresheet.scoresheet_id'))
    time = db.Column(db.Time)
    reported_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    match_id = db.Column(db.Integer, db.ForeignKey('match.match_id'))


class Scoresheet(db.Model):
    scoresheet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    reports = db.relationship("Report")


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

from addresses import address as address_bp
app.register_blueprint(address_bp)

from spots import spot as spot_bp
app.register_blueprint(spot_bp)

from photos import photo as photo_bp
app.register_blueprint(photo_bp)

from schedules import schedule as schedule_bp
app.register_blueprint(schedule_bp)

from bookings import booking as booking_bp
app.register_blueprint(booking_bp)

from teams import team as team_bp
app.register_blueprint(team_bp)


@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    asked_group = request.args.get("user_group")
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    result = User.query.filter_by(username=auth.username, group_id= asked_group).first()

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


if __name__ == '__main__':
    app.run()
