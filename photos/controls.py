import os
import uuid

import boto3

from core import db, Photo

S3_KEY = os.environ.get('KEY_ID')
S3_SECRET = os.environ.get('ACCESS_KEY')
s3 = boto3.resource('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
bucket = os.environ.get('BUCKET')


def save_photo(file, user_id=None, spot_id=None):
    filename = str(uuid.uuid4()) + "." + file.filename.rsplit('.', 1)[1].lower()
    if user_id is not None:
        s3.Bucket(bucket).put_object(Key=filename, Body=file)
        new_photo = Photo(user_id=user_id, filename=filename)
        db.session.add(new_photo)
    if spot_id is not None:
        s3.Bucket(bucket).put_object(Key=filename, Body=file)
        new_photo = Photo(spot_id=spot_id, filename=filename)
        db.session.add(new_photo)
    db.session.commit()
