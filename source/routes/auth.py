
from fastapi import APIRouter, Depends, HTTPException
from  pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal
from typing import Annotated
from models import models
from datetime import timedelta, datetime
from jose import jwt, JWTError
from starlette import status
from schemas import schema


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

SECRET_KEY = '0b93cd32d2ccbc99e6da76afe12ff6260142a34fe2b692062a8a2d6ee965c6c5';
ALGORITHM = 'HS256';

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


class Token(BaseModel):
    access_token: str
    token_type: str
    
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[SessionLocal, Depends(get_db)]

def authenticated_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False    
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')



@router.post("/auth/", tags=['Auth'], status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_req: schema.CreateUser):
            
    user_model_db = models.Users(
        email = create_user_req.email,
        username = create_user_req.username,
        first_name = create_user_req.first_name,
        last_name = create_user_req.last_name,       
        hashed_password = bcrypt_context.hash(create_user_req.password),
        role = create_user_req.role,
        is_active = True
    )
    
    db.add(user_model_db)
    db.commit()
    db.refresh(user_model_db)
 
    return user_model_db

    
@router.post("/auth/token", tags=['Auth'], response_model=Token)
async def login_for_acces_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    
    user = authenticated_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    
    token =  create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return { 
            'access_token': token,
            'token_type': 'bearer'
            }