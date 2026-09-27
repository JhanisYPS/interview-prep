from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    user_id: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int
    price: float
   
    class Config:
        from_attributes = True 

class ResponseOrderSchema(BaseModel):
    total : float
    status : str
    itens : List[OrderItemSchema]

    class Config:
        from_attributes = True 