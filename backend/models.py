from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, index=True)
    password_hash = Column(String)
    voice_embedding = Column(LargeBinary)
    balance = Column(Integer,default=5000)

    first_name = Column(String)
    last_name = Column(String)
    
    