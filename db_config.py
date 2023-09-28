import sqlalchemy as db 
from sqlalchemy import Table, Column, Integer, String, select

#параметры коннекта
login = 'postgres'
password = 'admin'
host = 'localhost'
db_name = 'restaurant_api'

metadata = db.MetaData()

#контейнер Menu
menus = Table('menus', metadata,
	Column('menu_id', Integer, primary_key=True),
	Column('title', String(120), nullable=False),
	Column('description', String(300), nullable=False)
)

#коннект
#db_connection = engine.connect()

#класс для передачи модели таблицы, требуется запроса
class DataBase:
	def __init__(self, model=None):
		engine = db.create_engine(f"postgresql+psycopg2://{login}:{password}@{host}/{db_name}")
		metadata.create_all(engine)
		
		self.connection = engine.connect()
		if model == 'menu':
			self.model = menus



#Достать записи
#test_list = []
#r = db_connection.execute(select(menus.c.title, menus.c.description))
#for row in r:
#	test_list.append(({'title':row[0]}, {'description': row[1]}))
#print(test_list)

#test = menus.insert().values(title='ete', description='erer')
#db_connection.execute(test)
#db_connection.commit()