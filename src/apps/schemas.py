
from pydantic import BaseModel, Field,ConfigDict

class productResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    model_config = {"from_attributes": True}

class productsResponse(BaseModel):
    products: list["productResponse"]
    model_config = {"from_attributes": True}

class LoginResponse(BaseModel):
    user: "UserResponse"
    access_token: str
    token_type: str = "bearer"
    # model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str 
    email: str 
    password: str=Field(..., min_length=6, max_length=72, description="Password must be between 6 and 72 characters long")

class UserLogin(BaseModel):
    email: str 
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # model_config = ConfigDict(from_attributes=True)
    model_config = {"from_attributes": True}



class productCreate(BaseModel):
    name: str 
    description: str
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)



class orderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0)
    total_amount: float = Field(..., gt=0)
    status: str = Field(..., min_length=1, max_length=50)

class orderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str
    model_config = {"from_attributes": True}

class cartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0)

class cartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = {"from_attributes": True}