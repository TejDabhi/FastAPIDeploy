from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils

router=APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_crendentials:schemas.UserLogin,db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_crendentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Crendentials1")
    if not utils.verify(user_crendentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Crendentials2")
    #create token
    #return token
    return {'token': 'example token'}
