from pydantic import BaseModel, EmailStr, Field


class ClientRequest(BaseModel):
    username : str = Field( default="marks", max_length=50)
    email: EmailStr = Field( default='mark23tes@gmail.com')
    phone: str = Field(default='7123442401', min_length=1, max_length=10)
    first_name: str = Field(default='Marco A',)
    last_name: str = Field(default='Mendoza')
    village: str = Field(default='Ejido, Palmillas')
    is_active: bool


class CreateUser(BaseModel):
    username: str = Field(default='Markuz', max_length=40)
    email: str =  Field(default='user@mail.com')
    first_name: str = Field('Marco')
    last_name: str = Field('Lopez')
    password: str = Field('12345678')
    role: str =  Field('admin')
    
    class config:
      orm_mode = True