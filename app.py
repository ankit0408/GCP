
# # API to search for addresses using a string
# @app.route('/api/search_address', methods=['GET'])
# def search_address():
#     search_string = request.args.get('search_string')
#     session = Session()

#     # Query the database for matching addresses
#     matched_contacts = session.query(Contact).filter(Contact.addresses.any(Contact.address_line_1.like(f'%{search_string}%'))).all()
#     session.close()

#     if not matched_contacts:
#         return jsonify({'error': 'No matching addresses found'}), 404

#     # Extract the matched address_line_1 values and create a list
#     matched_addresses = [address['address_line_1'] for contact in matched_contacts for address in contact.addresses]
#     return jsonify({'matched_addresses': matched_addresses})

# # API to store a new contact with phone number and addresses in the database
# @app.route('/api/store_contact', methods=['POST'])
# def store_contact():
#     data = request.get_json()

#     # Extract data from the request
#     phone_number = data.get('phone_number')
#     addresses = data.get('addresses')
#     full_address = "; ".join([", ".join(address.values()) for address in addresses])

#     # Create a new Contact object and store it in the database
#     new_contact = Contact(phone_number=phone_number, addresses=addresses, full_address=full_address)
#     session = Session()
#     session.add(new_contact)
#     session.commit()
#     session.close()

#     return jsonify({'message': 'Contact stored successfully'}), 201


from flask import Flask
from models import Base, create_engine
from routes.phone_numbers_routes import phone_routes
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Replace 'postgresql://username:password@localhost:5432/your_database_name' with your actual PostgreSQL connection URL
engine = create_engine('postgresql://postgres:postgres@localhost:5432/hackathon')
Base.metadata.create_all(engine)

app.register_blueprint(phone_routes)

if __name__ == "__main__":
    app.run(debug=True)



