import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.environ.get('DEBUG')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')

db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'PickUp API'


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

from matches import match as match_bp
app.register_blueprint(match_bp)

from players import player as player_bp
app.register_blueprint(player_bp)

from referees import referee as referee_bp
app.register_blueprint(referee_bp)

from goalkeeper import goalkeeper as goalkeeper_bp
app.register_blueprint(goalkeeper_bp)

if __name__ == '__main__':
    app.run()
