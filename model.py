from pydantic import BaseModel


class Todo(BaseModel):
    nanoid: str
    title: str
    desc: str
    checked: bool
