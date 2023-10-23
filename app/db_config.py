import asyncio
import os

import sqlalchemy as db
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import backref, relationship

# параметры коннекта
db_host = os.environ.get('HOST')
db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')

metadata = db.MetaData()

# контейнер Menu
menus = Table('menus', metadata,
              Column('menu_id', Integer, primary_key=True),
              Column('title', String(120), nullable=False),
              Column('description', String(300), nullable=False),
              )

sub_menus = Table('sub_menus', metadata,
                  Column('sub_menu_id', Integer, primary_key=True),
                  Column('menu_id', Integer, ForeignKey(
                      'menus.menu_id', ondelete='CASCADE')),
                  Column('title', String(120), nullable=False),
                  Column('description', String(300), nullable=False)
                  )

dishes = Table('dishes', metadata,
               Column('dish_id', Integer, primary_key=True),
               Column('sub_menu_id', Integer, ForeignKey(
                   'sub_menus.sub_menu_id', ondelete='CASCADE')),
               Column('menu_id', Integer, ForeignKey(
                   'menus.menu_id', ondelete='CASCADE')),
               Column('title', String(120), nullable=False),
               Column('description', String(300), nullable=False),
               Column('price', DECIMAL(5, 2), nullable=False)
               )


class DataBase:

    async def async_connect(self):
        engine = create_async_engine(f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}', echo=True)
        async with engine.begin() as connection:
            await connection.run_sync(metadata.create_all)
        return engine
