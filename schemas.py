from pydantic import BaseModel

class TodoSchema(BaseModel):
    id : int
    title : str
    description : str
    priority : int
    complete : bool

    class Config:
        from_attributes = True