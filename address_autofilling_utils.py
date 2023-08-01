import re
import ast
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from prompts.AER_Only_Prompt import prompt as aer_prompt
from prompts.Entity_Matching_Prompt import prompt as entities_matching_prompt
from prompts.Reverse_AER import prompt as reverse_aer_prompt



def get_entity_ordering_dict():
    
    entity_ordering_dict = {
        "name": 0,
        "door": 1,
        "floor": 2,
        "building": 3,
        "road": 4,

        "sub_locality": 5,
        "village": 5,

        "tehsil": 6,
        "locality": 6,

        "city": 7,

        "district": 8,

        "state": 9,
        "country": 10,
        "pincode": 11,
        "landmark": 12
        
    }
    
    return entity_ordering_dict
        
        
        
def standardise_address(response, entity_ordering_dict):

    try:
    
        ordered_response = {}
        for key in response:
            if(entity_ordering_dict.get(key) != None):
                ordered_response[key] = entity_ordering_dict[key]
            else:
                continue
            
        ordered_response = dict(sorted(ordered_response.items(), key = lambda x: x[1], reverse=False))
        
        # print(ordered_response)
        
        for key in ordered_response:
            ordered_response[key] = response[key]
        

        return ordered_response
    
    except Exception as e:
        print("Issue in standardising response: ",  e)
        return None


def clean_response(text):
    """Clean PaLM2 response and convert it into a dictionary"""

    try:
        text = re.sub(r"\n", "", text)
        text = re.sub("output:", "", text)
        text = text.strip()
        text = ast.literal_eval(text)
        return text
    
    except Exception as e:
        print("Issue in cleaning response: ", e)
        return None
    
    
#########################################
### Entity Extraction
#########################################    

def extract_entities(user_address, prompt, model, parameters):
    """Extracts entities from user address"""

    user_input = 'input: <<<"source_address_entities" : ' + user_address + ">>>\n"
    output = "output: "

    response = model.predict(prompt = prompt + user_input + output,
        **parameters
    )
    
    response = clean_response(response.text)
    entity_ordering_dict = get_entity_ordering_dict()
    response = standardise_address(response, entity_ordering_dict)
    
    return response

    
#########################################
### Entity Matching
#########################################

def match_entities(client_entities, database_entities_dict, entities_matching_prompt,  model, parameters):
    """Extracts entities from user address"""
    
    if((client_entities is None) or (database_entities_dict is None) or
       (len(client_entities)==0) or (len(database_entities_dict)==0)):
        return None
    
    database_entities = list(database_entities_dict.keys())
    user_input = f'"""input: <<<client_entities: {client_entities}>>> \n <<<database_entities: {database_entities}>>>\n"""'
    output = "output: "


    response = model.predict(prompt = entities_matching_prompt + user_input + output,
        **parameters
    )
    
    response = clean_response(response.text)
    
    for key in response:
        response[key] = database_entities_dict.get(response[key],'')
    
    return response


def match_data_with_client_entities(source_address_entities, destination_address_entities_list, reverse_aer_prompt,  model, parameters):
    """Maps values from source_address_entities (dict) to items in destination_address_entities_list"""
    
    if((source_address_entities is None) or (destination_address_entities_list is None) or
       (len(source_address_entities)==0) or (len(destination_address_entities_list)==0)):
        return None
    
    # user_input = f'input: <<<"source_address_entities": {source_address_entities}>>> \n <<<"destination_address_entities": {destination_address_entities_list}>>>\n'
    # output = "output: "

    user_input = """input: <<<"source_address_entities": """ + str(source_address_entities) + """>>> \n<<<"destination_address_entities": """ + str(destination_address_entities_list) + ">>>\n"
    output = "output: "


    print("user input: ", user_input)

    response = model.predict(prompt = reverse_aer_prompt + user_input + output,
        **parameters
    )
    
    response = clean_response(response.text)
    
    if(response):
        return response
    
    return None



if __name__ == "__main__":
    parameters = {
        "temperature": 0.0,
        "max_output_tokens": 256,
        "top_p": 0.9,
        "top_k": 5
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")

    # user_address = """{28/4/45} Mypadu Road Near Rajgopal Rice Mill,nan,nan,nan,Nellore,Andhra Pradesh"""
    # user_address = """9 2  vakula malika  thirumazhisai street  east tambaram  chennai,nan,nan,nan,Kanchipuram,Tamil Nadu"""
    # user_address = """c/o Mr. Nand Lal Sharma K-151, Mali Mohalla, Krishna Ganj, Near Anasagar, Ajmer Rajasthan,nan,nan,nan,AJMER,Rajasthan"""
    user_address = """{847}  near navjivini school old sular VPO sular patiala,nan,nan,nan,patiala,Punjab"""
    user_address = """"Mahavir nagar malout ward {no.8} Gali no.3  ashok mehta gali,nan,nan,nan,malout,Punjab"""
    user_address = """Above Bank of Baroda  opposite police station  Kiratpur  Bijnor   Landmark Kiratpur,nan,nan,nan,Bijnor,Uttar Pradesh"""


    response = extract_entities(user_address,aer_prompt, model, parameters)

    if(response):
        print("\nExtract Entities Response: ", response)


        client_entities = ['name', 'pincode', 'flat', 'area', 'locality', 'state']

        # database_entities_dict = {'door_number': '103', 'floor': '1st', 'society': 'tirumala towers', 'locality': 'new indhara nager', 'city': 'tirupathi', 'state': 'andhra pradesh'}
        # database_entities_dict = {'society': '3g homes', 'locality': 'kadugodi', 'city': 'bangalore', 'state': 'karnataka', 'pincode': '560067'}
        database_entities_dict = response



        client_entities_mapping = match_entities(client_entities, database_entities_dict, entities_matching_prompt, model, parameters)
        print("\nOld Entities matching prompt response: ", client_entities_mapping)
        
        client_entities_mapping = match_data_with_client_entities(database_entities_dict, client_entities, reverse_aer_prompt, model, parameters)
        print("\nReverse AER prompt response: ", client_entities_mapping)
    






    
