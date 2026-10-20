from fastapi import Depends,status,HTTPException
from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .settings import settings

outh2_schema=OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expires_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token:str,crendentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get('user_id')
        if id is None:
            raise crendentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise crendentials_exception
    return token_data

def get_current_user(token:str=Depends(outh2_schema),db:Session=Depends(get_db)):
    crendentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'could not validate crendentials',headers={"WWW-Authenticate":"Beare"})

    token=verify_access_token(token,crendentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user 