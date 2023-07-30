from flask import jsonify, request
from models import Session, Addresses
from address_autofilling_utils import extract_entities, match_entities, match_data_with_client_entities
from vertexai.preview.language_models import TextGenerationModel

from prompts.AER_Only_Prompt import prompt as aer_prompt
from prompts.Entity_Matching_Prompt import prompt as entities_matching_prompt
from prompts.Reverse_AER import prompt as reverse_aer_prompt


parameters = {
        "temperature": 0.0,
        "max_output_tokens": 256,
        "top_p": 0.9,
        "top_k": 5
        }
model = TextGenerationModel.from_pretrained("text-bison@001")

### API 1 - GET API - 
def get_addresses_by_phone_number(phone_number):
    session = Session()

    try:
        addresses = session.query(Addresses).with_entities(Addresses.id, 
                                                           Addresses.complete_address, 
                                                           ).filter_by(
            phone_number_id = phone_number).all()
        
        print("addresses: " , addresses)
        if addresses:
            address_dict = {int(id):address for id, address in addresses}
            return jsonify(address_dict), 200
        else:
            return jsonify({'message': 'No addresses found for the phone number'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error occurred while fetching data'}), 500
    
    finally:
        session.close()


### API 2 - POST API - 
def get_entities_by_complete_address():

    ### Fetch entities corresponding to the id of the selected address

    try:
        session = Session()
        request_data = request.get_json()
        id = request_data.get("id")
        print("request: ", request_data)

        if(id==None):
            raise ValueError("id not present in the input")

        if(type(int(id)) != int):
            raise TypeError("Expected integer value for id")


        id = int(id)
        db_entities = session.query(Addresses).with_entities(Addresses.entities, 
                                                            ).filter_by(
                        id = id).first()
        
        if not db_entities:
            return jsonify({'message': 'Please provide a unique identifier of the address'}), 400

        db_entities = db_entities[0]

        print("database entities: ", db_entities)


        client_entities = request_data['client_entities']    
        # client_entities = client_entities.split(',')
        print("client entities: " ,client_entities)


        ### Prompt: Matching database entitity names with client entities
        # client_entities_mapping = match_entities(client_entities, db_entities, entities_matching_prompt, model, parameters)
        
        ### Prompt: Matching Database entities with values directly with client_entities
        client_entities_mapping = match_data_with_client_entities(db_entities, client_entities, reverse_aer_prompt, model, parameters)
        
        print(client_entities_mapping)

        # Call text-bison here for entity extraction for the required form.

        # Sample response, assuming entities is a list of extracted entities.
        # Replace this with the actual response as per your requirement.
        return jsonify(client_entities_mapping), 200
        # else:
        #     return jsonify({'message': 'Complete address not found'}), 404
    except Exception as e:
        print(e)

        return jsonify({'message': 'Error occurred while fetching data'}), 500
    finally:
        session.close()


### API 3 - POST API - Store user's address
def store_address():
    data = request.get_json()
    phone_number_str = data.get('phone')

    input_payload = str(data)

    complete_address = ", ".join([str(data[key]) for key in data if((data[key]) and (key != "phone"))])
    print("complete_address: ", complete_address)

    print("\nconcatenated address:" , input_payload)
    entities = extract_entities(input_payload, aer_prompt, model, parameters)
    
    print("\nEntities: ", entities)


    session = Session()

    address_table_entry = Addresses(
                            phone_number_id=phone_number_str,
                            entities = entities,
                            complete_address = complete_address,
                            input_payload = input_payload)

    session.add(address_table_entry)

    session.commit()
    session.close()

    return jsonify({"message": "Address table entry saved successfully."}), 201
