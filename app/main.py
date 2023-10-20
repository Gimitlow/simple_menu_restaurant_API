from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from schemas import Menu, SubMenu, Dish
from crud import CRUD
import json

app = FastAPI()
crud = CRUD()

#МЕНЮ 
#Просмотр списка меню
@app.get("/api/v1/menus", status_code=200)
def get_menus():
	records = crud._MenuInterface().menu_get()
	if records:
		return records
	else:
		return []

#просмотр определенного меню
@app.get("/api/v1/menus/{menus_id}")
def get_menu_record(menus_id: int):
	result = crud._MenuInterface().menu_get(menus_id)
	return result

#добавление меню
@app.post("/api/v1/menus", status_code=201)
def add_new_menu_record(menu: Menu):
	result = crud._MenuInterface(menu.title, menu.description).menu_add_record()
	return result

#обновление записи меню
@app.patch("/api/v1/menus/{menus_id}", status_code=200)
def update_menu_record(menus_id: int, menu: Menu):
	print(menus_id)
	result = crud._MenuInterface(menu.title, menu.description).menu_update_record(menus_id)
	return result

#удаление записи меню 
@app.delete("/api/v1/menus/{menus_id}", status_code=200)
def delete_menu_record(menus_id: str):
	print(menus_id)
	result = crud._MenuInterface().menu_delete_record(menus_id)
	return result

# ПОДМЕНЮ 
#получение записей подменю
@app.get("/api/v1/menus/{menus_id}/submenus")
def get_submenus(menus_id: int):
	records = crud._SubMenuInterface().submenu_get(menus_id)
	return records

#получение определенной записи подменю
@app.get("/api/v1/menus/{menus_id}/submenus/{submenus_id}")
def get_submenu_record(menus_id: int, submenus_id: int):
	records = crud._SubMenuInterface().submenu_get(menus_id, submenus_id)
	return records

#добавление подменю в базу
@app.post("/api/v1/menus/{menus_id}/submenus")
def add_new_submenu_record(menus_id: int, submenu: SubMenu):
	result = crud._SubMenuInterface(submenu.title, submenu.description).submenu_add_record(menus_id)
	return result

#обновление записи подменю
@app.patch("/api/v1/menus/{menus_id}/submenus/{submenus_id}")
def update_submenu_record(menus_id: int, submenus_id: int, submenu: SubMenu):
	result = crud._SubMenuInterface(submenu.title, submenu.description).submenu_update_record(menus_id, submenus_id)
	return result

#удаление записи
@app.delete("/api/v1/menus/{menus_id}/submenus/{submenus_id}")
def delete_submenu_record(menus_id: int, submenus_id: int):
	result = crud._SubMenuInterface().submenu_delete_record(menus_id, submenus_id)
	return result

# БЛЮДА
#посмотреть все блюда
@app.get("/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes")
def get_dishes(menus_id: int, submenus_id: int):
	result = crud._DishesInteface().dish_get(menus_id, submenus_id)
	return result

#посмотреть определенное блюдо
@app.get("/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes/{dishes_id}")
def get_dish_record(menus_id: int, submenus_id: int, dishes_id: int):
	result = crud._DishesInteface().dish_get(menus_id, submenus_id, dishes_id)
	return result

#добавить блюдо
@app.post("/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes")
def add_new_dish(menus_id: int, submenus_id: int, dish: Dish):
	result = crud._DishesInteface(dish.title, dish.description, dish.price).dish_add_record(menus_id, submenus_id)
	return result

#обновить блюдо
@app.patch("/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes/{dishes_id}")
def update_dish_record(menus_id: int, submenus_id: int, dishes_id: int, dish: Dish):
	result = crud._DishesInteface(dish.title, dish.description, dish.price).dish_update_record(menus_id, submenus_id, dishes_id)
	return result

#удалить блюдо
@app.delete("/api/v1/menus/{menus_id}/submenus/{submenus_id}/dishes/{dishes_id}")
def delete_dish_record(menus_id: int, submenus_id: int, dishes_id: int):
	result = crud._DishesInteface().dish_delete_record(menus_id, submenus_id, dishes_id)
	return result