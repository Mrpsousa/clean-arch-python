import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
# from sqlalchemy.orm import relationship
from src.infra.config import Base


class AnimalTypes(enum.Enum):

    dog = "dog"
    cat = "cat"
    fish = "fish"
    turtle = "turtle"
    
class Pets(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    specie = Column(Enum(AnimalTypes), nullable=False)  
    age = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __rep__(self):
        return f"Pet [name = {self.name}, espicie = {self.specie}, user_id = {self.user_id}]"