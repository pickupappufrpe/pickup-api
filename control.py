from flask import request
from core import app, User
from functools import wraps
import jwt


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
