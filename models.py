from sqlalchemy import Column, Integer, String, JSON, create_engine, ForeignKey
from sqlalchemy import Column, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.event import listen
from sqlalchemy.sql.functions import func
from sqlalchemy import Column, Integer, UniqueConstraint
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/hackathon')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# class PhoneNumbers(Base):
#     __tablename__ = 'phone_numbers'

#     phone_number_id = Column(Integer, primary_key=True)
#     phone_number = Column(String, nullable=False, unique=True)
#     owner_name = Column(String)

#     # Establish the one-to-many relationship between PhoneNumbers and Addresses
#     addresses = relationship('Addresses', back_populates='phone_number', cascade='all, delete-orphan')

# id = Column(Integer, primary_key=True)
#     col1 = Column(Integer, unique=True, nullable=False)
#     col2 = Column(Integer)
#     parent_id = Column(Integer, ForeignKey('my_table.id'))
#     children = relationship('MyTable', backref='parent', remote_side=[id])

class Addresses(Base):
    __tablename__ = 'addresses'

    id = Column(Integer , primary_key=True)
    address_id = Column(Integer)
    phone_number_id = Column(String, nullable=False)
    entities = Column(JSON, nullable=False)
    complete_address = Column(String, nullable=False)
    input_payload = Column(JSON, nullable=False)

    ### Unique Constraint: We can have multiple address_ids corresponding to a phone number.
    __table_args__ = (UniqueConstraint(phone_number_id, address_id),)

    @staticmethod
    def increment(mapper, connection, address):
        last = (
            session.query(func.max(Addresses.address_id))
            .filter(Addresses.phone_number_id == address.phone_number_id)
            .scalar()
        )
        address.address_id = 1 + (last if last else 0)

listen(Addresses, "before_insert", Addresses.increment)
session.close()


    # Establish the relationship between Addresses and PhoneNumbers
    #phone_number = relationship('PhoneNumbers', back_populates='addresses')

# Replace 'postgresql://username:password@localhost:5432/your_database_name' with your actual PostgreSQL connection URL



