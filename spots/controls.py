from core import db, Address, Contact, Spot, Ground, Schedule, City, State, Photo


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


def get_schedules(spot_id):
    schedules = Schedule.query.filter_by(spot_id=spot_id)
    schedules_data = []
    for i in schedules:
        schedules_data.append({'week_day': i.week_day,
                               'opening_time': str(i.opening_time),
                               'closing_time': str(i.closing_time)})
    return schedules_data


def get_address(address_id):
    address = Address.query.filter_by(id=str(address_id)).first()
    city = City.query.filter_by(id=address.city_id).first()
    state = State.query.filter_by(id=city.state_id).first()

    return {'street': address.street,
            'number': address.number,
            'neighborhood': address.neighborhood,
            'city': city.name,
            'state': state.name,
            'cep': address.cep}


def get_contact(contact_id):
    contact = Contact.query.filter_by(id=contact_id).first()
    return {'email': contact.email,
            'phone': contact.phone}


def get_photo_list(spot_id):
    target = Photo.query.filter_by(spot_id=spot_id)
    photo_list = []
    for i in target:
        photo_list.append({"filename": i.image})
    return photo_list


def render_spot(spot):
    schedules_data = get_schedules(spot.id)
    address_data = get_address(spot.address_id)
    contact_data = get_contact(spot.contact_id)
    ground = Ground.query.filter_by(ground_id=spot.ground_id).first()
    photo_list = get_photo_list(spot.id)

    spot_data = {'id': spot.id,
                 'name': spot.name,
                 'price': spot.price,
                 'ground': ground.name,
                 'owner_id': spot.owner_id,
                 'contact_id': spot.contact_id,
                 'schedules': schedules_data,
                 'address': address_data,
                 'contact': contact_data,
                 'photos': photo_list}
    return spot_data


def render_spot_group(spots):
    output = []
    for s in spots:
        output.append(render_spot(s))
    return {'spots': output}


def get_spot_by_id_query(spot_id):
    target = Spot.query.filter_by(id=spot_id).first()

    if not target:
        return {'message': 'Spot not found!'}

    return render_spot(target)
