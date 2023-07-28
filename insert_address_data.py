from models import Addresses, PhoneNumbers, Session

if __name__ == '__main__':

    #query to get data asscocited with a phone number in PhoneNumbers table
    session = Session()
    #contacts = session.query(PhoneNumbers).filter_by(phone_number = '7450288661').first()
    session.query(PhoneNumbers).filter_by(phone_number = '7450288661').first()
    #print(contacts)
    session.close()


    # Create a new adress object with the data to insert
    new_contact_data = {
        'phone_number_id': '745',
        'entities': 
          {
"flat": "9",
"floor": "second",
"wing": "a",
"society": "paryavaran complex",
"road": "ignou road",
"landmark": "bikaner wali road",
"city": "new delhi",
"state": "delhi"
},
        'complete_address': 'D-5Flat no.9(Second floor)Wing-AParyavaran complex IGNOU road  Bikaner wali road,nan,nan,nan,New Delhi,Delhi',
    }

    # Create a new Contact object
    new_contact = Addresses(**new_contact_data)

    # Open a session and add the new Contact object
    session = Session()
    session.add(new_contact)

    # Commit the session to save the changes to the database
    session.commit()

    # Close the session
    session.close()

