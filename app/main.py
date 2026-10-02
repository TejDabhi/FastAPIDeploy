from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas,utils
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id: {id} not found")
    return post

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.Create_Post,db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist")
    db.delete(post)
    db.commit()
    return None

@app.put("/posts/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_post(id: int,post: schemas.Post,db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} not found")
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    new_user = models.User(email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}',response_model=schemas.UserOut)
def get_users(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Detail of the User id : {id} not found")
    return user 