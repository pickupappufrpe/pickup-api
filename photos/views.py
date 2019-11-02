from . import photo

from core import db, Photo, User, Spot, token_required, app
from flask import request, send_file, Response
import boto3
import os
import uuid

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
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return {'message': 'No file part'}
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'message': 'No selected file'}
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + "." + file.filename.rsplit('.', 1)[1].lower()
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            s3.Bucket(bucket).put_object(Key=filename, Body=file)
            new_photo = Photo(spot_id=spot_id, image=filename)
            db.session.add(new_photo)
            db.session.commit()
            return {'message': 'Success!'}


@photo.route('/spot/<user_id>/photo', methods=['POST'])
@token_required
def upload_user_photo(current_user, user_id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return {'message': 'No file part'}
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'message': 'No selected file'}
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + "." + file.filename.rsplit('.', 1)[1].lower()
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            s3.Bucket(bucket).put_object(Key=filename, Body=file)
            new_photo = Photo(user_id=user_id, image=filename)
            db.session.add(new_photo)
            db.session.commit()
            return {'message': 'Success!'}


@photo.route('/spot/<spot_id>/photo/list', methods=['GET'])
@token_required
def get_spot_photo_list(current_user, spot_id):
    target = Photo.query.filter_by(spot_id=spot_id)
    photo_list = []
    for i in target:
        photo_list.append({"filename": i.image})
    return {'spot_photos': photo_list}


@photo.route('/user/<user_id>/photo/list', methods=['GET'])
@token_required
def get_user_photo_list(current_user, user_id):
    target = Photo.query.filter_by(user_id=user_id)
    photo_list = []
    for i in target:
        photo_list.append({i.id: i.image})
    return {'user_photos': photo_list}


@photo.route('/photo/<filename>', methods=['GET'])
@token_required
def get_photo_by_filename(current_user, filename):
    # path = app.config['UPLOAD_FOLDER']+'/'+filename

    my_bucket = s3.Bucket(bucket)

    file_obj = my_bucket.Object(filename).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='image/jpeg',
        # headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


@photo.route('/user/<user_id>/photo', methods=['POST'])
@token_required
def save_user_photo(current_user):
    data = request.get_json()
    new_photo = Photo(user_id=current_user.id,
                      image=data['image'])
    db.session.add(new_photo)
    db.session.commit()
    return {'message': 'Image saved!'}
