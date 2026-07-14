from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    email : str
    username : str
    created_at : datetime
    updated : datetime

class UserPostRequest(BaseModel):
    content : str

class UserPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id : int
    username : str
    id : int
    content : str
    created_at : datetime