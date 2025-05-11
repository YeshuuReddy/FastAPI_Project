from fastapi import FastAPI
import models
from database import engine
from routers import auth,todos

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

"""


from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel,Field
from database import SessionLocal,engine
from sqlalchemy.orm import Session
import models
from models import Todos
from typing import Annotated
app=FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    id:int
    title:str=Field(min_length=3)
    description:str=Field(min_length=5)
    priority:int=Field(gt=0,lt=6)
    complete:bool

db_dependency=Annotated[Session,Depends(get_db)]
@app.get("/tasks")
async def read_tasks(db:db_dependency):
    todos=db.query(Todos).all()
    if todos is not None:
        return todos
    raise HTTPException(status_code=404,detail='item not found')

@app.get("/tasks/{task_id}")
async def task_by_id(task_id:int,db:db_dependency):
    todos=db.query(Todos).filter(Todos.id==task_id).first()
    if todos is not None:
        return todos
    raise HTTPException(status_code=404,detail='item not found')

@app.post("/tasks/create_task")
async def create_new_task(create_task:TodoRequest,db:db_dependency):
    #todos=Todos(id=create_task.id,title=create_task.title,description=create_task.description,priority=create_task.priority,complete=create_task.complete)
    todos=Todos(**create_task.model_dump())
    db.add(todos)
    db.commit()
    
"""

