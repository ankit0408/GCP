from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, JSON, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


# Create the SQLAlchemy engine and session
engine = create_engine('postgresql://postgres:postgres@localhost:5432/hackathon')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)

# Define the table schema with a self-referential relationship
class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    col1 = Column(Integer, nullable=False)
    col2 = Column(Integer)
    parent_id = Column(Integer, ForeignKey('my_table.id'))
    children = relationship('MyTable', backref='parent', remote_side=[id])

# Create the table
Base.metadata.create_all(engine)


# Create a session
#session = Session()

# Insert data into the table
entry1 = MyTable(col1=100, col2=200)
entry2 = MyTable(col1=100, col2=300)
entry3 = MyTable(col1=200, col2=400)
session.add_all([entry1, entry2, entry3])

# Commit the changes to the database
session.commit()