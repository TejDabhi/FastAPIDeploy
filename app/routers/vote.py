from fastapi import FastAPI, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from ..database import get_db
  
router=APIRouter(
    prefix='/votes',
    tags=['Votes']
)


@router.post("",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post With id : {vote.post_id} Not Exist")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if(vote.dir):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"USer {current_user.id} has already voted on post {vote.id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote Does Not Exist")
        db.delete(found_vote)
        db.commit()
        return {"message":"successfully delete vote"}