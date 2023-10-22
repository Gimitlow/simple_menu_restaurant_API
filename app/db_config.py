import sqlalchemy as db 
from sqlalchemy import Table, Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, backref
import os

#параметры коннекта
db_host = os.environ.get('HOST')
db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
#f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
#f"postgresql://admin:admin@localhost:5432/restuarant_api"

metadata = db.MetaData()

#контейнер Menu
menus = Table('menus', metadata,
	Column('menu_id', Integer, primary_key=True),
	Column('title', String(120), nullable=False),
	Column('description', String(300), nullable=False),
)

sub_menus = Table('sub_menus', metadata,
	Column('sub_menu_id', Integer, primary_key=True),
	Column('menu_id', Integer, ForeignKey('menus.menu_id', ondelete="CASCADE")),
	Column('title', String(120), nullable=False),
	Column('description', String(300), nullable=False)
)

dishes = Table('dishes', metadata,
	Column('dish_id', Integer, primary_key=True),
	Column('sub_menu_id', Integer, ForeignKey('sub_menus.sub_menu_id', ondelete="CASCADE")),
	Column('menu_id', Integer, ForeignKey('menus.menu_id', ondelete="CASCADE")),
	Column('title', String(120), nullable=False),
	Column('description', String(300), nullable=False),
	Column('price', DECIMAL(5,2), nullable=False)
)

#коннект
#db_connection = engine.connect()

#класс для передачи копии модели таблицы, требуется для генерации запроса
class DataBase:
	def __init__(self, model=None):
		engine = db.create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}")
		metadata.create_all(engine)
		
		self.connection = engine.connect()
		if model == 'menu':
			self.model = menus
		elif model == 'sub_menu':
			self.model = sub_menus
		elif model == 'dish':
			self.model = dishes