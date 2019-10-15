from . import contact

from flask import request
from core import User, Contact, db, token_required


@contact.route('/contact', methods=['POST'])
@token_required
def create_contact():
    data = request.get_json()
    target = Contact(email=data['email'], phone=data['phone'])
    db.session.add(target)
    db.session.flush()
    new_contact_id = str(target.id)
    db.session.commit()
    return {'message': 'New Contact created!', "contact_id": new_contact_id}


@contact.route('/user/<user_id>/contact', methods=['POST'])
@token_required
def set_contact(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    target = Contact.query.filter_by(id=data['contact_id']).first()
    user.contact_id = target.id
    db.session.add(user)
    db.session.commit()
    return {'message': "Contact has been set!"}


@contact.route('/user/<user_id>/contact', methods=['GET'])
@token_required
def get_contact(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()
    target = Contact.query.filter_by(id=user.contact_id).first()

    if not target:
        return {'message': "Contact not found!"}

    return {'email': target.email, 'phone': target.phone}