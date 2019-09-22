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
    login = db.Column(db.String(50))
    password = db.Column(db.String(100))


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
        except:
            return {'message': 'Token is invalid!'}, 401

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    search = User.query.filter_by(login=data['login']).first()
    if search is None:
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(login=data['login'], password=hashed_password)
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
        user_data['login'] = user.login

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
    user_data['name'] = user.login


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

    user = User.query.filter_by(login=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : str(user.id), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return {'token' : token.decode('UTF-8')}

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

if __name__ == '__main__':
    app.run()
