from . import photo

from core import db, Photo, User, Spot, token_required, app
from flask import request, send_file
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@photo.route('/spot/<spot_id>/photo', methods=['POST'])
@token_required
def upload_file(current_user, spot_id):
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_photo = Photo(spot_id=spot_id, image=filename)
            db.session.add(new_photo)
            db.session.commit()
            return {'message': 'Success!'}
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))


@photo.route('/spot/<spot_id>/photo/list', methods=['GET'])
@token_required
def get_photo_list(current_user, spot_id):
    target = Photo.query.filter_by(spot_id=spot_id)
    photo_list = []
    for i in target:
        photo_list.append({i.id: i.image})
    return {'spots': photo_list}


@photo.route('/photo/<filename>', methods=['GET'])
@token_required
def get_photo_by_filename(current_user, filename):
    path = app.config['UPLOAD_FOLDER']+'/'+filename

    return send_file(path, mimetype='image/gif')


@photo.route('/spot/<spot_id>/photo', methods=['GET'])
@token_required
def get_spot_photo(current_user, spot_id):
    target = Photo.query.filter_by(spot_id=spot_id).first()
    filename = app.config['UPLOAD_FOLDER']+'/'+target.image
    if not target:
        return {'message': 'No photo found!'}

    return send_file(filename, mimetype='image/gif')


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
