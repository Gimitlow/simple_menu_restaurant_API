from db_config import DataBase
from sqlalchemy import select
from fastapi.responses import JSONResponse
from sqlalchemy.orm import relationship

menu_table = DataBase('menu')
submenu_table = DataBase('sub_menu')
dish_table = DataBase('dish')

class CRUD:

	#интерфейс таблицы Menu
	class _MenuInterface:

		#конструктор Меню
		def __init__(self, title=None, description=None):
			self.title = title
			self.description = description

		def menu_get(self, id=None):
			global menu_table
			connection = DataBase().connection
			
			response = []

			request = connection.execute(select(menu_table.model.c.menu_id, menu_table.model.c.title, menu_table.model.c.description))
			for row in request:
				if id is None:
					menu_list = {}
					submenu_count = connection.execute(select(submenu_table.model).where(submenu_table.model.c.menu_id == row[0])).all()
					dish_count = connection.execute(select(dish_table.model).where(dish_table.model.c.menu_id == row[0])).all()
					
					menu_list['id'] = str(row[0])
					menu_list['title'] = row[1]
					menu_list['description'] = row[2]
					menu_list['submenus_count'] = len(submenu_count)
					menu_list['dishes_count'] = len(dish_count)

					response.append(menu_list)
				elif id == row[0]:
					menu_list = {}
					submenu_count = connection.execute(select(submenu_table.model).where(submenu_table.model.c.menu_id == id)).all()
					dish_count = connection.execute(select(dish_table.model).where(dish_table.model.c.menu_id == id)).all()
					
					menu_list['id'] = str(row[0])
					menu_list['title'] = row[1]
					menu_list['description'] = row[2]
					menu_list['submenus_count'] = len(submenu_count)
					menu_list['dishes_count'] = len(dish_count)
					
					connection.close()
					return JSONResponse(content=menu_list, status_code=200)

			if response:
				connection.close()
				return JSONResponse(content=response, status_code=200)
			elif id:
				connection.close()
				response = {}
				response['detail'] = 'menu not found'
				return JSONResponse(content=response, status_code=404)
			else:
				connection.close()
				return JSONResponse(content=[], status_code=200)

		def menu_add_record(self):
			global menu_table
			connection = DataBase().connection

			request = menu_table.model.insert().values(title=self.title, description=self.description)
			connection.execute(request)
			connection.commit()
			connection.close()
			return f'Меню {self.title} успешно добавлено'

		def menu_update_record(self, id=None):
			global menu_table
			connection = DataBase().connection

			request = menu_table.model.update().where(menu_table.model.c.menu_id==id).values(title=self.title, description=self.description)

			connection.execute(request)
			connection.commit()
			connection.close()
			return f'Запись Меню Id:{id} обнавлена'

		def menu_delete_record(self, id: int):
			global menu_table
			connection = DataBase().connection

			connection.execute(dish_table.model.delete().where(dish_table.model.c.menu_id == id))
			connection.execute(submenu_table.model.delete().where(submenu_table.model.c.menu_id == id))
			connection.execute(menu_table.model.delete().where(menu_table.model.c.menu_id == id))

			connection.commit()
			connection.close()
			return f'Запись Меню Id:{id} удалена'

	class _SubMenuInterface:

		#конструктор подменю
		def __init__(self, title=None, description=None):
			self.title = title
			self.description = description

		def submenu_get(self, menu_id, submenu_id=None):
			global submenu_table
			connection = DataBase().connection
			response = []

			dish_count = connection.execute(select(dish_table.model).where(dish_table.model.c.menu_id == menu_id, dish_table.model.c.sub_menu_id == submenu_id)).all()

			if submenu_id is None:
				request = connection.execute(select(submenu_table.model.c.sub_menu_id, submenu_table.model.c.menu_id, submenu_table.model.c.title, submenu_table.model.c.description).where(submenu_table.model.c.menu_id == menu_id)).all()
				for row in request:
					dish_count = connection.execute(select(dish_table.model).where(dish_table.model.c.menu_id == row[1], dish_table.model.c.sub_menu_id == row[0])).all()
					submenus_list = {}
					
					submenus_list['id'] = str(row[0])
					submenus_list['menu_id'] = row[1]
					submenus_list['title'] = row[2]
					submenus_list['description'] = row[3]
					submenus_list['dishes_count'] = len(dish_count)

					response.append(submenus_list)
			else:
				request = connection.execute(select(submenu_table.model.c.sub_menu_id, submenu_table.model.c.menu_id, submenu_table.model.c.title, submenu_table.model.c.description).where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenu_id)).all()
				for row in request:
					submenus_list = {}
					dish_count = connection.execute(select(dish_table.model).where(dish_table.model.c.menu_id == menu_id, dish_table.model.c.sub_menu_id == submenu_id)).all()
					
					submenus_list['id'] = str(row[0])
					submenus_list['menu_id'] = row[1]
					submenus_list['title'] = row[2]
					submenus_list['description'] = row[3]
					submenus_list['dishes_count'] = len(dish_count)

					return submenus_list

			if response:
				return JSONResponse(content=response, status_code=201)
			elif submenu_id:
				connection.close()
				response = {}
				response['detail'] = 'submenu not found'
				return JSONResponse(content=response, status_code=404)
			else:
				connection.close()
				return JSONResponse(content=[], status_code=200)

		def submenu_add_record(self, menu_id=None):
			global submenu_table
			connection = DataBase().connection

			r = connection.execute(select(menu_table.model.c.menu_id)).scalars().all()
			if menu_id not in r:
				return JSONResponse(content=f'Нету Меню по Id:{menu_id} к которому можно создать Подменю', status_code=201)

			request = connection.execute(submenu_table.model.select().where(submenu_table.model.c.menu_id == menu_id))
			for row in request:
				if self.title == row[2]:
					print(row[2])
					return JSONResponse(content=f'Подменю с названием {self.title} уже присутствует в Меню Id:{menu_id}', status_code=201)

			request = submenu_table.model.insert().values(menu_id=menu_id, title=self.title, description=self.description)
			connection.execute(request)
			connection.commit()
			connection.close()
			return JSONResponse(content=f'Подменю {self.title} успешно добавлено', status_code=201)

		def submenu_update_record(self, menu_id: int, submenus_id: int):
			global submenu_table
			connection = DataBase().connection

			result = connection.execute(select(submenu_table.model).where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenus_id)).scalars().all()

			if not result:
				connection.close()
				return f'Не найдено Подменю Id:{submenus_id} в Меню по Id:{menu_id}'

			request = submenu_table.model.update().where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenus_id).values(title=self.title, description=self.description)
			r = connection.execute(request)
			connection.commit()
			connection.close()

			return f'Запись Подменю Id:{submenus_id} в Меню Id:{menu_id} обнавлена'

		def submenu_delete_record(self, menu_id: int, submenus_id: int):
			global submenu_table
			connection = DataBase().connection

			#request = connection.execute(submenu_table.model.delete().where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenus_id))
			#r = connection.execute(request)

			connection.execute(dish_table.model.delete().where(dish_table.model.c.menu_id == menu_id, dish_table.model.c.sub_menu_id == submenus_id))
			connection.execute(submenu_table.model.delete().where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenus_id))
			connection.commit()
			connection.close()
			return f'Запись Подменю Id:{submenus_id} удалена из Меню Id:{submenus_id}'

	class _DishesInteface:

		#конструктор блюда
		def __init__(self, title=None, description=None, price=None):
			self.title = title
			self.description = description
			self.price = price

		def dish_get(self, menu_id: int, submenus_id: int, dishes_id=None):
			global dish_table
			connection = DataBase().connection
			result = []

			if dishes_id is None:
				request = connection.execute(dish_table.model.select().where(dish_table.model.c.menu_id==menu_id, dish_table.model.c.sub_menu_id==submenus_id))
				for row in request:
					dish_list = {}

					dish_list['id'] = str(row[0])
					dish_list['sub_menu_id'] = str(row[1])
					dish_list['menu_id'] = str(row[2])
					dish_list['title'] = row[3]
					dish_list['description'] = row[4]
					dish_list['price'] = "%.2f" % row[5]

					result.append(dish_list)
			else:
				request = connection.execute(dish_table.model.select().where(dish_table.model.c.menu_id==menu_id, dish_table.model.c.sub_menu_id==submenus_id, dish_table.model.c.dish_id==dishes_id))
				for row in request:
					dish_list = {}

					dish_list['id'] = str(row[0])
					dish_list['sub_menu_id'] = str(row[1])
					dish_list['menu_id'] = str(row[2])
					dish_list['title'] = row[3]
					dish_list['description'] = row[4]
					dish_list['price'] = "%.2f" % row[5]

					return JSONResponse(content=dish_list, status_code=200)

			if result:
				connection.close()
				return JSONResponse(content=result, status_code=200)
			elif dishes_id:
				connection.close()
				response = {}
				response['detail'] = 'dish not found'
				return JSONResponse(content=response, status_code=404)				
			else:
				connection.close()
				return JSONResponse(content=[], status_code=200)

		def dish_add_record(self, menu_id: int, submenus_id: int):
			global dish_table
			connection = DataBase().connection

			request = connection.execute(select(submenu_table.model).where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenus_id)).all()
			if not request:
				return JSONResponse(content="Нету такого подменю и меню", status_code=200)			

			request = connection.execute(dish_table.model.select().where(dish_table.model.c.menu_id == menu_id))
			for row in request:
				if self.title == row[3]:
					print(row[3])
					return JSONResponse(content=f'Блюдо с названием {self.title} уже присутствует в Подменю Id{submenus_id}', status_code=201)

			request = dish_table.model.insert().values(sub_menu_id=submenus_id, menu_id=menu_id, title=self.title, description=self.description, price=self.price)
			
			connection.execute(request)
			connection.commit()
			connection.close()
			return JSONResponse(content=f'Блюдо {self.title} успешно добавлено в Меню Id:{menu_id}, Подменю Id:{submenus_id}', status_code=201)

		def dish_update_record(self, menu_id: int, submenus_id: int, dishes_id: int):
			global dish_table
			connection = DataBase().connection

			request = connection.execute(dish_table.model.select().where(dish_table.model.c.menu_id==menu_id, dish_table.model.c.sub_menu_id==submenus_id, dish_table.model.c.dish_id==dishes_id)).all()
			if not request:
				return f'Не найдено Блюдо Id:{submenus_id} в Подменю Id:{submenus_id} в Меню по Id:{menu_id}'

			request = dish_table.model.update().where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenus_id).values(title=self.title, description=self.description, price=self.price)
			result = connection.execute(request)
			connection.commit()
			connection.close()	

			return f'Обновлено Блюдо Id:{submenus_id} в Подменю Id:{submenus_id} в Меню по Id:{menu_id}'

		def dish_delete_record(self, menu_id: int, submenus_id: int, dishes_id: int):
			global dish_table
			connection = DataBase().connection

			request = connection.execute(dish_table.model.delete().where(dish_table.model.c.menu_id == menu_id, dish_table.model.c.sub_menu_id == submenus_id, dish_table.model.c.dish_id == dishes_id))
			connection.commit()
			connection.close()
			return f'Запись блюда Id:{dishes_id} успешно удалена из Меню Id:{menu_id}, Подменю Id:{submenus_id}'