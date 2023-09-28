from db_config import DataBase
from sqlalchemy import select
import json

menu_table = DataBase('menu')
submenu_table = DataBase('sub_menu')

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

			r = connection.execute(select(menu_table.model.c.menu_id, menu_table.model.c.title, menu_table.model.c.description))
			for row in r:
				if id is None:
					response.append([{'id':row[0]}, {'title':row[1]}, {'description': row[2]}])
				elif id == row[0]:
					response.append([{'id':row[0]}, {'title':row[1]}, {'description': row[2]}])
					connection.close()
					return response
			
			if response:
				connection.close()
				return response
			else:
				connection.close()
				return None

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
			return f'Запись {id} обнавлена'

		def menu_delete_record(self, id=None):
			global menu_table
			connection = DataBase().connection

			request = menu_table.model.delete().where(menu_table.model.c.menu_id == id)

			connection.execute(request)
			connection.commit()
			connection.close()
			return f'Запись {id} удалена'

	class _SubMenuInterface:

		#конструктор подменю
		def __init__(self, title=None, description=None):
			self.title = title
			self.description = description

		def submenu_get(self, menu_id, submenu_id=None):
			global submenu_table
			connection = DataBase().connection
			response = []

			if submenu_id is None:
				request = connection.execute(select(submenu_table.model.c.sub_menu_id, submenu_table.model.c.menu_id, submenu_table.model.c.title, submenu_table.model.c.description).where(submenu_table.model.c.menu_id == menu_id)).all()
				for row in request:
					response.append([{'id':row[0]}, {'menu_id':row[1]}, {'title': row[2]}, {'description': row[3]}])
			else:
				request = connection.execute(select(submenu_table.model.c.sub_menu_id, submenu_table.model.c.menu_id, submenu_table.model.c.title, submenu_table.model.c.description).where(submenu_table.model.c.menu_id == menu_id, submenu_table.model.c.sub_menu_id == submenu_id)).all()
				for row in request:
					response.append([{'id':row[0]}, {'menu_id':row[1]}, {'title': row[2]}, {'description': row[3]}])

			if response:
				return response
			else:
				return 'Подменю не найдено'

		def submenu_add_record(self, menu_id=None):
			global submenu_table
			connection = DataBase().connection

			r = connection.execute(select(menu_table.model.c.menu_id)).scalars().all()
			if menu_id not in r:
				return f'Нету меню по Id:{menu_id} к которому можно создать подменю'

			request = submenu_table.model.insert().values(menu_id=menu_id, title=self.title, description=self.description)
			connection.execute(request)
			connection.commit()
			connection.close()
			return f'Подменю {self.title} успешно добавлено'

		def submenu_update_record(self):
			pass

		def submenu_delete_record(self):
			pass