from fastapi import FastAPI,Depends, HTTPException
from starlette.status import HTTP_200_OK
import models
from models import Todos
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
# from schemas import TodoSchema
# from starlette import status
# from typing import List

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title:str=Field(min_length=5)
    description:str=Field(min_length=10)
    priority:int=Field(gt=0,lt=6)
    complete:bool



@app.get("/items/",status_code=HTTP_200_OK)
def get_items(db: Session = Depends(get_db)):
    todos= db.query(Todos).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No items found")
    return todos

@app.get("/items/{todo_id}",status_code=HTTP_200_OK)
def get_items_by_id(todo_id:int,db: Session=Depends(get_db)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException (status_code=404, detail='Todo not found')



@app.post("/items/create_todo")
def create_todo(todo_request:TodoRequest,db:Session=Depends(get_db)):
    todo_model=Todos(title=todo_request.title,description=todo_request.description,priority=todo_request.priority,complete=todo_request.complete)
    db.add(todo_model)
    db.commit()