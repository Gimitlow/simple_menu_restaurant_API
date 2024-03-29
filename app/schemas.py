from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str


class SubMenu(BaseModel):
    title: str
    description: str


class Dish(BaseModel):
    title: str
    description: str
    price: float
