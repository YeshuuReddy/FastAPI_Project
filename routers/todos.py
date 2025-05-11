from fastapi import APIRouter,Depends, HTTPException
from starlette.status import HTTP_200_OK
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from typing import Annotated

router=APIRouter()

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


db_dependency=Annotated[Session,Depends(get_db)]

@router.get("/items/",status_code=HTTP_200_OK)
def get_items(db: Session = Depends(get_db)):
    todos= db.query(Todos).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No items found")
    return todos

@router.get("/items/{todo_id}",status_code=HTTP_200_OK)
def get_items_by_id(todo_id:int,db: Session=Depends(get_db)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException (status_code=404, detail='Todo not found')



@router.post("/items/create_todo")
def create_todo(todo_request:TodoRequest,db:Session=Depends(get_db)):
    todo_model=Todos(title=todo_request.title,description=todo_request.description,priority=todo_request.priority,complete=todo_request.complete)
    db.add(todo_model)
    db.commit()

@router.put("/tasks/update_the_task/{task_id}")
async def update_the_task(db:db_dependency,task_id:int,update_task:TodoRequest):
    todos=db.query(Todos).filter(Todos.id==task_id).first()
    if todos is None:
        raise HTTPException(status_code=404,detail="task_id doesnt match")

    todos.id=update_task.id
    todos.title=update_task.title
    todos.description=update_task.description
    todos.priority=update_task.priority
    todos.complete=update_task.complete

    db.add(todos)
    db.commit()


@router.delete("/tasks/delete_the_task/{task_id}")
async def delete_the_task(db:db_dependency,
                          task_id:int):
    todos=db.query(Todos).filter(Todos.id==task_id).first()
    if todos is None:
        raise HTTPException(status_code=404,detail="task to delete is not found")

    db.query(Todos).filter(Todos.id==task_id).delete()
    db.commit()
