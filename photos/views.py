from . import photo

from core import db, Photo, User, Spot, token_required
from flask import request


@photo.route('/spot/<spot_id>/photo', methods=['POST'])
@token_required
def save_spot_photo(current_user):
    data = request.get_json()
    new_photo = Photo(spot_id=data['spot_id'],
                      image=data['image'])
    db.session.add(new_photo)
    db.session.commit()
    return {'message': 'Image saved!'}


@photo.route('/spot/<spot_id>/photo', methods=['GET'])
@token_required
def get_spot_photo(current_user, spot_id):
    target = Photo.query.filter_by(spot_id=spot_id).first()

    if not target:
        return {'message': 'No photo found!'}

    return {'image': target.image}


@photo.route('/user/<user_id>/photo', methods=['POST'])
@token_required
def save_user_photo(current_user):
    data = request.get_json()
    new_photo = Photo(user_id=current_user.id,
                      image=data['image'])
    db.session.add(new_photo)
    db.session.commit()
    return {'message': 'Image saved!'}


@photo.route('/user/<user_id>/photo', methods=['GET'])
@token_required
def get_user_photo(current_user, user_id):
    target = Photo.query.filter_by(user_id=user_id).first()

    if not target:
        return {'message': 'No photo found!'}

    return {'image': target.image}
