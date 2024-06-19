from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Clients(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String)
    phone = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    village = Column(String)
    is_active = Column(Boolean, default=True)
