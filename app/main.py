import asyncio
import json

from crud import CRUD
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from schemas import Dish, Menu, SubMenu

app = FastAPI()
crud = CRUD()


# МЕНЮ
# Просмотр списка меню
@app.get('/api/v1/menus', status_code=200)
async def get_menus():
    result = await crud._MenuInterface().menu_get()
    # records = crud._MenuInterface().menu_get()
    if result:
        return result
    else:
        return []


# просмотр определенного меню
@app.get('/api/v1/menus/{menus_id}')
async def get_menu_record(menus_id: int):
    result = await crud._MenuInterface().menu_get(menus_id)
    return result


# добавление меню
@app.post('/api/v1/menus', status_code=201)
async def add_new_menu_record(menu: Menu):
    result = await crud._MenuInterface(menu.title, menu.description).menu_add_record()
    return result


# обновление записи меню
@app.patch('/api/v1/menus/{menus_id}', status_code=200)
async def update_menu_record(menus_id: int, menu: Menu):
    result = await crud._MenuInterface(menu.title, menu.description).menu_update_record(menus_id)
    return result


# удаление записи меню
@app.delete('/api/v1/menus/{menus_id}', status_code=200)
async def delete_menu_record(menus_id: str):
    result = await crud._MenuInterface().menu_delete_record(int(menus_id))
    return result


# ПОДМЕНЮ
# получение записей подменю
@app.get('/api/v1/menus/{menus_id}/submenus')
async def get_submenus(menus_id: int):
    print("ok")
    records = await crud._SubMenuInterface().submenu_get(menus_id)
    return records


# получение определенной записи подменю
@app.get('/api/v1/menus/{menus_id}/submenus/{submenus_id}')
async def get_submenu_record(menus_id: int, submenus_id: int):
    records = await crud._SubMenuInterface().submenu_get(menus_id, submenus_id)
    return records


# добавление подменю в базу
@app.post('/api/v1/menus/{menus_id}/submenus')
async def add_new_submenu_record(menus_id: int, submenu: SubMenu):
    result = await crud._SubMenuInterface(submenu.title, submenu.description).submenu_add_record(menus_id)
    return result


# обновление записи подменю
@app.patch('/api/v1/menus/{menus_id}/submenus/{submenus_id}')
async def update_submenu_record(menus_id: int, submenus_id: int, submenu: SubMenu):
    result = await crud._SubMenuInterface(submenu.title, submenu.description).submenu_update_record(menus_id, submenus_id)
    return result


# удаление записи
@app.delete('/api/v1/menus/{menus_id}/submenus/{submenus_id}')
async def delete_submenu_record(menus_id: int, submenus_id: int):
    result = await crud._SubMenuInterface().submenu_delete_record(menus_id, submenus_id)
    return result


# БЛЮДА
# посмотреть все блюда
@app.get('/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes')
async def get_dishes(menus_id: int, submenus_id: int):
    result = await crud._DishesInteface().dish_get(menus_id, submenus_id)
    return result


# посмотреть определенное блюдо
@app.get('/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes/{dishes_id}')
async def get_dish_record(menus_id: int, submenus_id: int, dishes_id: int):
    result = await crud._DishesInteface().dish_get(menus_id, submenus_id, dishes_id)
    return result


# добавить блюдо
@app.post('/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes')
async def add_new_dish(menus_id: int, submenus_id: int, dish: Dish):
    result = await crud._DishesInteface(dish.title, dish.description, dish.price).dish_add_record(menus_id, submenus_id)
    return result


# обновить блюдо
@app.patch('/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes/{dishes_id}')
async def update_dish_record(menus_id: int, submenus_id: int, dishes_id: int, dish: Dish):
    result = await crud._DishesInteface(dish.title, dish.description, dish.price).dish_update_record(
        menus_id, submenus_id, dishes_id)
    return result


# удалить блюдо
@app.delete('/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes/{dishes_id}')
async def delete_dish_record(menus_id: int, submenus_id: int, dishes_id: int):
    result = await crud._DishesInteface().dish_delete_record(menus_id, submenus_id, dishes_id)
    return result
