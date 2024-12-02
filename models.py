from pydantic import BaseModel, Field
from typing import Optional

class AddressModel(BaseModel):
    city: str
    country: str

class StudentCreateModel(BaseModel):
    name: str
    age: int
    address: AddressModel

class StudentResponseModel(BaseModel):
    id: str
