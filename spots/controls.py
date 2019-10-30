from core import db, Address, Contact, Spot


def create_address_query(city_id, street, cep, number, neighborhood):
    new_address = Address(street=street,
                          cep=cep,
                          number=number,
                          neighborhood=neighborhood,
                          city_id=city_id)
    db.session.add(new_address)
    db.session.flush()
    db.session.commit()
    return new_address.id


def create_contact_query(email, phone):
    new_contact = Contact(email=email,
                          phone=phone)
    db.session.add(new_contact)
    db.session.flush()
    db.session.commit()
    return new_contact.id


def create_spot_query(spot_name, price, ground_id, owner_id, address_id, contact_id):
    new_spot = Spot(owner_id=owner_id,
                    name=spot_name,
                    price=price,
                    address_id=address_id,
                    contact_id=contact_id,
                    ground_id=ground_id)
    db.session.add(new_spot)
    db.session.flush()
    db.session.commit()
    return new_spot.id
