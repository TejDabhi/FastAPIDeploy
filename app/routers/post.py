from fastapi import FastAPI, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from ..database import get_db

router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id: {id} not found")
    return post

@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.Create_Post,db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    print(get_current_user)
    new_post = models.Post(owner_id=get_current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist")
    # We need conditition user delete their own post
    if post.owner_id!=get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You Cannot Delete Other's Post")
    db.delete(post)
    db.commit()
    return None

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_post(id: int,post: schemas.Post,db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} not found")
    # We need conditition user delete their own post
    if post.owner_id!=get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You Cannot Delete Other's Post")
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post
