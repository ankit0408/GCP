from flask import jsonify, request
from models import Session, PhoneNumbers, Addresses


def get_addresses_by_phone_number(phone_number):
    session = Session()
    try:
        phone_entry = session.query(PhoneNumbers).filter_by(
            phone_number=phone_number).first()
        if not phone_entry:
            return jsonify({'message': 'Phone number not found'}), 404

        addresses = session.query(Addresses).with_entities(Addresses.complete_address).filter_by(
            phone_number_id=phone_entry.phone_number_id).all()
        if addresses:
            address_list = [addr[0] for addr in addresses]
            return jsonify(address_list), 200
        else:
            return jsonify({'message': 'No addresses found for the phone number'}), 404
    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching data'}), 500
    finally:
        session.close()


def get_entities_by_complete_address():
    complete_address = request.args.get('complete_address')

    if not complete_address:
        return jsonify({'message': 'Please provide a complete_address as a query parameter'}), 400

    session = Session()
    try:
        address_entry = session.query(Addresses).filter_by(
            complete_address=complete_address).all()
        if address_entry:
            # Assuming 'entities' is a property of the 'Addresses' model, adjust this line if necessary.
            entities = [addr.entities for addr in address_entry]
            # Call text-bison here for entity extraction for the required form.

            # Sample response, assuming entities is a list of extracted entities.
            # Replace this with the actual response as per your requirement.
            return jsonify(entities), 200
        else:
            return jsonify({'message': 'Complete address not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching data'}), 500
    finally:
        session.close()


def store_contact():
    data = request.get_json()
    phone_number_str = data.get('phone')
    owner_name = data.get('name')

    address_parts = [value for value in data.values()
                     if isinstance(value, str)]
    complete_address = ", ".join(filter(None, address_parts))

    session = Session()

    phone_number = session.query(PhoneNumbers).filter_by(
        phone_number=phone_number_str).first()
    
    if not phone_number:
        phone_number = PhoneNumbers(
            phone_number=phone_number_str, owner_name=owner_name)
        session.add(phone_number)
        session.commit()
        phone_number = session.query(PhoneNumbers).filter_by(
            phone_number=phone_number_str).first()

    # Create the entry in Addresses table with dynamic JSON data
    address = Addresses(phone_number_id=phone_number.phone_number_id,
                        entities=data, complete_address=complete_address)
    session.add(address)
    session.commit()
    session.close()

    return jsonify({"message": "Address added successfully."}), 201
