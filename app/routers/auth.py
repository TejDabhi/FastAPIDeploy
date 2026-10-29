from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_crendentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_crendentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Crendentials1")
    if not utils.verify(user_crendentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Crendentials2")
    #create token
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    #return token
    return {'access_token': access_token,"token_type":"bearer"}
