# routes/phone_numbers_routes.py
from flask import Blueprint
from controllers.phone_numbers_controller import get_addresses_by_phone_number, get_entities_by_complete_address, store_address, update_address

# Define the phone_routes blueprint
phone_routes = Blueprint('phone_routes', __name__)

# Define the route for getting addresses by phone number
phone_routes.route('/api/phone_numbers/<phone_number>/addresses', methods=['GET'])(get_addresses_by_phone_number)

# Define the route for getting entities by complete address
phone_routes.route('/api/addresses/entities', methods=['POST'])(get_entities_by_complete_address)

# Define the route for storing the user address
phone_routes.route('/api/store_address', methods=['POST'])(store_address)

# Define the route for updating the user address
phone_routes.route('/api/store_address/<address_id>', methods=['PUT'])(update_address)
