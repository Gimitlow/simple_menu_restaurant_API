from db_config import DataBase
from sqlalchemy import select
import json

class CRUD:

	#интерфейс таблицы Menu
	class _MenuInterface:

		def __init__(self, title=None, description=None):
			self.title = title
			self.description = description

		def menu_get(self, id=None):
			menu_table = DataBase('menu')
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
				return f'Меню не найдено.'

		def menu_add_record(self):
			menu_table = DataBase('menu')
			connection = DataBase().connection

			request = menu_table.model.insert().values(title=self.title, description=self.description)
			connection.execute(request)
			connection.commit()
			connection.close()
			return "Успешно добавлено"

		def menu_update_record(self, id=None):
			menu_table = DataBase('menu')
			connection = DataBase().connection

			request = menu_table.model.update().where(menu_table.model.c.menu_id==id).values(title=self.title, description=self.description)
			connection.execute(request)
			connection.commit()
			connection.close()
			return f'Запись {id} обнавлена'

		def menu_delete_record(self, id=None):
			menu_table = DataBase('menu')
			connection = DataBase().connection

			request = menu_table.model.delete().where(menu_table.model.c.menu_id == id)

			connection.execute(request)
			connection.commit()
			connection.close()
			return f'Запись {id} удалена'