import random
import string
from models import PhoneNumbers, Session

# if __name__ == '__main__':
    # Create a new Contact object with the data to insert
    # new_contact_data = {
    #     'phone_number_id': 1,
    #     'phone_number': '+1234567890',
    #     'addresses': [
    #         {
    #             'address_line_1': '123 Main Street',
    #             'address_line_2': 'Apt 4B',
    #             'city': 'Anytown',
    #             'state': 'NY',
    #             'postal_code': '12345',
    #             'country': 'United States'
    #         },
    #         {
    #             'address_line_1': '456 Elm Avenue',
    #             'city': 'Otherville',
    #             'state': 'CA',
    #             'postal_code': '98765',
    #             'country': 'United States'
    #         }
    #     ],
    #     'full_address': '123 Main Street, Apt 4B, Anytown, NY, 12345, United States; 456 Elm Avenue, Otherville, CA, 98765, United States'
    # }

    # # Create a new Contact object
    # new_contact = Contact(**new_contact_data)

    # # Open a session and add the new Contact object
    # session = Session()
    # session.add(new_contact)

    # # Commit the session to save the changes to the database
    # session.commit()

    # # Close the session
    # session.close()

print("hello world")
def generate_random_phone_number():
    prefix = random.choice(['6', '7', '8', '9'])
    print(prefix)
    suffix = ''.join(random.choices(string.digits, k=9))
    print(suffix)
    return prefix + suffix

def generate_random_owner_name():
    names = [
    "Aarav",
    "Aishwarya",
    "Akshay",
    "Ananya",
    "Arjun",
    "Chahat",
    "Devika",
    "Gaurav",
    "Ishika",
    "Kabir",
    "Kavya",
    "Manish",
    "Neha",
    "Pranav",
    "Rajesh",
    "Sakshi",
    "Sandeep",
    "Tanvi",
    "Uday",
    "Vidya"
]
    surnames = [
    "Patel",
    "Sharma",
    "Chowdhury",
    "Kumar",
    "Gupta",
    "Singh",
    "Mukherjee",
    "Verma",
    "Rao",
    "Joshi",
    "Rathod",
    "Choudhary",
    "Malhotra",
    "Pandey",
    "Shah",
    "Reddy",
    "Shinde",
    "Iyer",
    "Sinha",
    "Nair"
    ]
    name = random.choice(names)
    surname = random.choice(surnames)
    return f"{name} {surname}"

if __name__ == "__main__":
    session = Session()

    try:
        # Populating 400 data entries in PhoneNumbers table
        for _ in range(400):
            print('1')
            phone_number = generate_random_phone_number()
            print('2')
            owner_name = generate_random_owner_name()

            phone_entry = PhoneNumbers(phone_number=phone_number, owner_name=owner_name)
            session.add(phone_entry)
        
        session.commit()
        print("Data successfully populated.")
    except Exception as e:
        session.rollback()
        print("Error occurred:", e)
    finally:
        session.close()