from models import Base, engine

if __name__ == '__main__':
    # Create the Contacts table in the database
    Base.metadata.create_all(engine)

