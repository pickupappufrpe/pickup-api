from core import db


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
    goalkeepers = db.relationship("Goalkeeper", uselist=False)
    referees = db.relationship("Referee", uselist=False)
    players = db.relationship("Player", uselist=False)
    bookings = db.relationship("Booking")
    matches = db.relationship("Match")
    captains = db.relationship("Team")


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
    average_rating = db.Column(db.Float, default=0)
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
    filename = db.Column(db.String(40))


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
    referee_id = db.Column(db.Integer, db.ForeignKey('referee.referee_id'))
    goalkeeper_id = db.Column(db.Integer, db.ForeignKey('goalkeeper.goalkeeper_id'))
    lineups = db.relationship('Lineup')
    player_invites = db.relationship('PlayerInvite')
    referee_invites = db.relationship('RefereeInvite')
    goalkeeper_invites = db.relationship('GoalkeeperInvite')


class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    captain_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'))
    average_rating = db.Column(db.Float, default=0)
    matches_count = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    ratings = db.relationship("PlayerRating")
    lineups = db.relationship("Lineup")
    guests = db.relationship("PlayerInvite", foreign_keys='PlayerInvite.guest_id')
    hosts = db.relationship("PlayerInvite", foreign_keys='PlayerInvite.host_id')
    reported = db.relationship("Report", foreign_keys='Report.reported_id')
    reporters = db.relationship("Report", foreign_keys='Report.reporter_id')


class Goalkeeper(db.Model):
    goalkeeper_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    average_rating = db.Column(db.Float, default=0)
    matches_count = db.Column(db.Integer)
    ratings = db.relationship("GoalkeeperRating")
    invites = db.relationship("GoalkeeperInvite")
    bookings = db.relationship("Booking")


class Referee(db.Model):
    referee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    average_rating = db.Column(db.Float, default=0)
    matches_count = db.Column(db.Integer)
    ratings = db.relationship("RefereeRating")
    invites = db.relationship("RefereeInvite")
    bookings = db.relationship("Booking")


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


class GoalkeeperRating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    goalkeeper_id = db.Column(db.Integer, db.ForeignKey('goalkeeper.goalkeeper_id'))
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class RefereeRating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    referee_id = db.Column(db.Integer, db.ForeignKey('referee.referee_id'))
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    reports = db.relationship("Report")


class Lineup(db.Model):
    lineup_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'))


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


class PlayerInvite(db.Model):
    playerinvite_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    host_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'))
    status = db.Column(db.Boolean, default=False)
    answered = db.Column(db.Boolean, default=False)


class RefereeInvite(db.Model):
    refereeinvite_id = db.Column(db.Integer, primary_key=True)
    referee_id = db.Column(db.Integer, db.ForeignKey('referee.referee_id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'))
    status = db.Column(db.Boolean)
    answered = db.Column(db.Boolean, default=False)


class GoalkeeperInvite(db.Model):
    goalkeeperinvite_id = db.Column(db.Integer, primary_key=True)
    goalkeeper_id = db.Column(db.Integer, db.ForeignKey('goalkeeper.goalkeeper_id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'))
    status = db.Column(db.Boolean)
    answered = db.Column(db.Boolean, default=False)