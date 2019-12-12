import os

import boto3
from flask import request, Response

from controllers import token_required
from models import Photo
from photos.controls import save_photo
from . import photo

S3_KEY = os.environ.get('KEY_ID')
S3_SECRET = os.environ.get('ACCESS_KEY')
s3 = boto3.resource('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
bucket = os.environ.get('BUCKET')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@photo.route('/spot/<spot_id>/photo', methods=['POST'])
@token_required
def upload_spot_photo(current_user, spot_id):
    # check if the post request has the file part
    if 'file' not in request.files:
        return {'message': 'No file part'}
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return {'message': 'No selected file'}
    if file and allowed_file(file.filename):
        save_photo(file, spot_id=spot_id)
        return {'message': 'Success!'}


@photo.route('/user/<user_id>/photo', methods=['POST'])
@token_required
def upload_user_photo(current_user, user_id):
    # check if the post request has the file part
    if 'file' not in request.files:
        return {'message': 'No file part'}
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return {'message': 'No selected file'}
    if file and allowed_file(file.filename):
        save_photo(file, user_id=user_id)
        return {'message': 'Success!'}


@photo.route('/spot/<spot_id>/photo/list', methods=['GET'])
@token_required
def get_spot_photo_list(current_user, spot_id):
    target = Photo.query.filter_by(spot_id=spot_id)
    photo_list = []
    for i in target:
        photo_list.append({"filename": i.filename})
    return {'spot_photos': photo_list}


@photo.route('/user/photo/list', methods=['GET'])
@token_required
def get_user_photo_list(current_user):
    target = Photo.query.filter_by(user_id=current_user.id)
    photo_list = []
    for i in target:
        photo_list.append({"filename": i.filename})
    return {'user_photos': photo_list}


@photo.route('/photo/<filename>', methods=['GET'])
@token_required
def get_photo_by_filename(current_user, filename):
    my_bucket = s3.Bucket(bucket)
    file_obj = my_bucket.Object(filename).get()
    return Response(
        file_obj['Body'].read(),
        mimetype='image/jpeg',)
