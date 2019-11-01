from core import db, Address, Contact, Spot, Ground, Schedule, City, State


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


def get_spot_by_id_query(spot_id):
    target = Spot.query.filter_by(id=spot_id).first()

    if not target:
        return {'message': 'Spot not found!'}

    ground = Ground.query.filter_by(ground_id=target.ground_id).first()
    schedules = Schedule.query.filter_by(spot_id=spot_id)
    schedules_data = []
    for i in schedules:
        schedules_data.append({'week_day': i.week_day,
                               'opening_time': i.opening_time,
                               'closing_time': i.closing_time})

    address = Address.query.filter_by(id=str(target.address_id)).first()

    city = City.query.filter_by(id=address.city_id).first()
    state = State.query.filter_by(id=city.state_id).first()

    address_data = {
        'street': address.street,
        'number': address.number,
        'neighborhood': address.neighborhood,
        'city': city.name,
        'state': state.name,
        'cep': address.cep
    }

    return {'id': target.id,
            'name': target.name,
            'price': target.price,
            'ground': ground.name,
            'owner_id': target.owner_id,
            'contact_id': target.contact_id,
            'schedules': schedules_data,
            'address': address_data}
