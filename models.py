from sqlalchemy import Column, Integer, String, JSON, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class PhoneNumbers(Base):
    __tablename__ = 'phone_numbers'

    phone_number_id = Column(Integer, primary_key=True)
    phone_number = Column(String, nullable=False, unique=True)
    owner_name = Column(String)

    # Establish the one-to-many relationship between PhoneNumbers and Addresses
    addresses = relationship('Addresses', back_populates='phone_number', cascade='all, delete-orphan')

class Addresses(Base):
    __tablename__ = 'addresses'

    address_id = Column(Integer, primary_key=True)
    phone_number_id = Column(Integer, ForeignKey('phone_numbers.phone_number_id', ondelete='CASCADE'), nullable=False)
    entities = Column(JSON, nullable=False)
    complete_address = Column(String, nullable=False)

    # Establish the relationship between Addresses and PhoneNumbers
    phone_number = relationship('PhoneNumbers', back_populates='addresses')

# Replace 'postgresql://username:password@localhost:5432/your_database_name' with your actual PostgreSQL connection URL
engine = create_engine('postgresql://postgres:postgres@localhost:5432/hackathon')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


