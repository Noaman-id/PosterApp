from pydantic import BaseModel

class UserAuthLoginRequest(BaseModel):
    email : str
    password : str

class UserAuthRegisterRequest(BaseModel):
    email : str
    username : str
    password : str

class UserPasswordRequest(BaseModel):
    email : str

class UserChangePassword(BaseModel):
    email: str
    security_code : str
    new_password : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str