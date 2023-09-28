from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from schemas import Menu 
from crud import CRUD

app = FastAPI()
crud = CRUD()

#Просмотр списка меню
@app.get("/api/v1/menus")
def get_menus():
	records = crud._MenuInterface().menu_get()
	result = sorted(records, key= lambda x: x[0]['id'], reverse=False)
	return result

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
	result = crud._MenuInterface(menu.title, menu.description).menu_update_record(menus_id)
	return result

#удаление записи меню 
@app.delete("/api/v1/menus/{menus_id}", status_code=200)
def delete_menu_record(menus_id: int):
	result = crud._MenuInterface().menu_delete_record(menus_id)
	return result

#получение записей подменю
@app.get("api/v1/{menus_id}/submenus")
def get_submenu_records():
	return "test"

#получение определенной записи подменю
@app.get("api/v1/{menus_id}/submenus/{summenus_id}")
def get_submenu_record():
	return "test"