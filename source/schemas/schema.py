from pydantic import BaseModel, EmailStr, Field


class ClientRequest(BaseModel):
    username : str = Field( default="marks", max_length=50)
    email: EmailStr = Field( default='mark23tes@gmail.com')
    phone: str = Field(default='7123442401', min_length=1, max_length=10)
    first_name: str = Field(default='Marco A',)
    last_name: str = Field(default='Mendoza')
    village: str = Field(default='Ejido, Palmillas')
    is_active: bool