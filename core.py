from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(100))


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    # TODO: senha_criptografada = gerar_senha_criptografada(data['password'])

    new_user = User(login=data['login'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'New user created!'}

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['login'] = user.login
        user_data['password'] = user.password

        output.append(user_data)

    return {'users' : output}


@app.route('/user/<id>', methods=['GET'])
def get_one_user(id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return {'message' : 'No user found!'}

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.login
    user_data['password'] = user.password

    return {'user': user_data}

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return {'message': 'No user found!'}

    db.session.delete(user)
    db.session.commit()

    return {'message': 'The user has been deleted!'}

if __name__ == '__main__':
    app.run()