from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import models
from schemas import schema
from database import SessionLocal

router = APIRouter(
    prefix='/clientes',
    tags=['Clientes']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        
        
db_dependency = Annotated[SessionLocal, Depends(get_db)]

@router.get('/', status_code=status.HTTP_200_OK)
async def get_clients(db: db_dependency):
    return db.query(models.Clients).all()


@router.get('/id/{client_id}', status_code=status.HTTP_200_OK)
async def get_client_by_id(db: db_dependency, client_id: int = Path(gt=0)):
    client_model = db.query(models.Clients).filter(models.Clients.id == client_id).first()    
    
    if client_model is not None:
        return client_model
    raise HTTPException(status_code=404, detail='Client not found')


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_client(db: db_dependency, client_request: schema.ClientRequest):    
    client_model = models.Clients(**client_request.dict())
    print(client_model)
    db.add(client_model)
    db.commit()
    db.refresh(client_model)
    return client_model

@router.put('/update/{client_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_client(db: db_dependency, client_request: schema.ClientRequest, client_id: int = Path(gt=0)):
    
    client_model = db.query(models.Clients).filter(models.Clients.id == client_id).first()    
    
    if client_model is None:
        raise HTTPException(status_code=404, detail='Client no found')
    
    
    client_model.email = client_request.email,
    client_model.username = client_request.username,
    client_model.phone = client_request.phone,
    client_model.first_name = client_request.first_name,
    client_model.last_name = client_request.last_name,
    client_model.village = client_request.village,
    db.add(client_model)
    db.commit()
    return client_model

@router.delete('/delete/{client_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(db: db_dependency, client_id: int = Path(gt=0)):
    
    client_model = db.query(models.Clients).filter(models.Clients.id == client_id ).first()
    
    if client_model is not None:
        db.delete(client_model)
        db.commit()
        return client_model
    raise HTTPException(status_code=404, detail='Client not found')
