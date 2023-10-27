import asyncio

from cache_engine import RedisMemCache
from db_config import DataBase, dishes, menus, sub_menus
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import relationship

# глобальные экземпляры
db = DataBase()
redis_cache = RedisMemCache()


class CRUD:

    # интерфейс таблицы Menu
    class _MenuInterface:

        # конструктор Меню
        def __init__(self, title=None, description=None):
            self.title = title
            self.description = description

        # получение всех записей меню либо по id
        async def menu_get(self, id=None):
            response = []

            # проверка редис
            if id:
                cache = await redis_cache._MenuMemCache().cache_get_menu(str(id))

            engine = await db.async_connect()

            async with engine.begin() as conn:
                request = await conn.execute(select(menus.c.menu_id, menus.c.title, menus.c.description))

                for row in request:
                    if id is None:
                        menu_list = {}
                        submenu_count = await conn.execute(select(sub_menus).where(sub_menus.c.menu_id == row[0]))
                        dish_count = await conn.execute(select(dishes).where(dishes.c.menu_id == row[0]))

                        menu_list['id'] = str(row[0])
                        menu_list['title'] = row[1]
                        menu_list['description'] = row[2]
                        menu_list['submenus_count'] = len(
                            submenu_count.fetchall())
                        menu_list['dishes_count'] = len(dish_count.fetchall())

                        await redis_cache._MenuMemCache().cache_set_menu(str(row[0]), menu_list)
                        response.append(menu_list)

                    elif id == row[0]:
                        menu_list = {}
                        submenu_count = await conn.execute(select(sub_menus).where(sub_menus.c.menu_id == id))
                        dish_count = await conn.execute(select(dishes).where(dishes.c.menu_id == id))

                        menu_list['id'] = str(row[0])
                        menu_list['title'] = row[1]
                        menu_list['description'] = row[2]
                        menu_list['submenus_count'] = len(
                            submenu_count.fetchall())
                        menu_list['dishes_count'] = len(dish_count.fetchall())

                        await engine.dispose()
                        await redis_cache._MenuMemCache().cache_set_menu(id, menu_list)
                        return JSONResponse(content=menu_list, status_code=200)

                if response:
                    await engine.dispose()
                    return JSONResponse(content=response, status_code=200)
                elif id:
                    await engine.dispose()
                    response = {}
                    response['detail'] = 'menu not found'
                    return JSONResponse(content=response, status_code=404)
                else:
                    await engine.dispose()
                    return JSONResponse(content=[], status_code=200)

        # Добавление нового меню
        async def menu_add_record(self):
            engine = await db.async_connect()

            async with engine.begin() as conn:
                request = await conn.execute(menus.insert().values(title=self.title, description=self.description))

                req = await conn.execute(select(menus.c.menu_id, menus.c.title, menus.c.description).order_by(menus.c.menu_id.desc()))
                record = req.first()
                response = {
                    'id': str(record[0]),
                    'title': record[1],
                    'description': record[2]
                }

                await engine.dispose()
                return JSONResponse(content=response, status_code=201)

    # Обновление записи по id
        async def menu_update_record(self, id=None):
            engine = await db.async_connect()

            async with engine.begin() as conn:
                request = await conn.execute(menus.update().where(menus.c.menu_id == id).values(title=self.title, description=self.description))

                await redis_cache._MenuMemCache().cache_update_menu(id, self.title, self.description)

                await engine.dispose()
                return f'Запись Меню Id:{id} обнавлена'

    # Удаление записи по id
        async def menu_delete_record(self, id: int):
            engine = await db.async_connect()

            async with engine.begin() as conn:
                await conn.execute(dishes.delete().where(dishes.c.menu_id == id))
                await conn.execute(sub_menus.delete().where(sub_menus.c.menu_id == id))
                await conn.execute(menus.delete().where(menus.c.menu_id == id))

                await engine.dispose()

                return f'Запись Меню Id:{id} удалена'

    # Интерфейс подменю
    class _SubMenuInterface:

        # конструктор подменю
        def __init__(self, title=None, description=None):
            self.title = title
            self.description = description

        # Получение подменю по ID либо все по ID меню
        async def submenu_get(self, menu_id: int, submenu_id=None):
            engine = await db.async_connect()

            response = []

            if menu_id and submenu_id:
                cache = await redis_cache._SubmenuMemCache().cache_get_submenu(
                    str(menu_id), str(submenu_id))
                if cache:
                    return cache

            async with engine.begin() as conn:
                dish_count = await conn.execute(select(dishes).where(dishes.c.menu_id == menu_id, dishes.c.sub_menu_id == submenu_id))

                if submenu_id is None:
                    request = await conn.execute(select(sub_menus.c.sub_menu_id, sub_menus.c.menu_id, sub_menus.c.title, sub_menus.c.description).where(sub_menus.c.menu_id == menu_id))
                    for row in request:
                        dish_count = await conn.execute(select(dishes).where(dishes.c.menu_id == row[1], dishes.c.sub_menu_id == row[0]))

                        submenus_list = {}
                        submenus_list['id'] = row[0]
                        submenus_list['menu_id'] = row[1]
                        submenus_list['title'] = row[2]
                        submenus_list['description'] = row[3]
                        submenus_list['dishes_count'] = len(
                            dish_count.fetchall())

                        await redis_cache._SubmenuMemCache().cache_set_submenu(str(row[0]), str(row[1]), submenus_list)
                        response.append(submenus_list)
                else:
                    request = await conn.execute(select(sub_menus.c.sub_menu_id, sub_menus.c.menu_id, sub_menus.c.title, sub_menus.c.description).where(sub_menus.c.menu_id == menu_id, sub_menus.c.sub_menu_id == submenu_id))
                    for row in request:

                        submenus_list = {}
                        dish_count = await conn.execute(select(dishes).where(dishes.c.menu_id == menu_id, dishes.c.sub_menu_id == submenu_id))

                        submenus_list['id'] = str(row[0])
                        submenus_list['menu_id'] = row[1]
                        submenus_list['title'] = row[2]
                        submenus_list['description'] = row[3]
                        submenus_list['dishes_count'] = len(
                            dish_count.fetchall())

                        await redis_cache._SubmenuMemCache().cache_set_submenu(str(row[0]), str(row[1]), submenus_list)
                        return JSONResponse(content=submenus_list, status_code=200)

                if response:
                    await engine.dispose()
                    return JSONResponse(content=response, status_code=200)
                elif submenu_id:
                    await engine.dispose()
                    response = {}
                    response['detail'] = 'submenu not found'
                    return JSONResponse(content=response, status_code=404)
                else:
                    await engine.dispose()
                    return JSONResponse(content=[], status_code=200)

        # Добавление подменю
        async def submenu_add_record(self, menu_id=None):
            engine = await db.async_connect()

            async with engine.begin() as conn:
                menu_nums = await conn.execute(select(menus.c.menu_id))

                if menu_id not in menu_nums.scalars():
                    return JSONResponse(content=f'Нету Меню по Id:{menu_id} к которому можно создать Подменю', status_code=201)

                request = await conn.execute(sub_menus.select().where(sub_menus.c.menu_id == menu_id))
                for row in request:
                    if self.title == row[2]:
                        return JSONResponse(content=f'Подменю с названием {self.title} уже присутствует в Меню Id:{menu_id}', status_code=201)

                request = await conn.execute(sub_menus.insert().values(menu_id=menu_id, title=self.title, description=self.description))

                record = await conn.execute(select(sub_menus.c.sub_menu_id, sub_menus.c.menu_id, sub_menus.c.title, sub_menus.c.description).where(sub_menus.c.menu_id == menu_id).order_by(sub_menus.c.sub_menu_id.desc()))
                rows = record.first()
                req_dish = await conn.execute(select(dishes).where(dishes.c.menu_id == menu_id, dishes.c.sub_menu_id == rows[0]))

                response = {
                    'id': str(rows[0]),
                    'menu_id': rows[1],
                    'title': rows[2],
                    'description': rows[3],
                    'dish_count': len(req_dish.fetchall())
                }

                await redis_cache._SubmenuMemCache().cache_set_submenu(
                    str(rows[0]), str(rows[1]), response)

                await engine.dispose()

                return JSONResponse(content=response, status_code=201)

        # обновление записи подменю
        async def submenu_update_record(self, menu_id: int, submenus_id: int):
            engine = await db.async_connect()

            async with engine.begin() as conn:
                result = await conn.execute(select(sub_menus).where(
                    sub_menus.c.menu_id == menu_id, sub_menus.c.sub_menu_id == submenus_id))

                if not result.scalars():
                    await engine.dispose()
                    return f'Не найдено Подменю Id:{submenus_id} в Меню по Id:{menu_id}'

                request = await conn.execute(sub_menus.update().where(sub_menus.c.menu_id == menu_id, sub_menus.c.sub_menu_id == submenus_id).values(title=self.title, description=self.description))

                await redis_cache._SubmenuMemCache().cache_update_submenu(
                    submenus_id, menu_id, self.title, self.description)

                await engine.dispose()
                return f'Запись Подменю Id:{submenus_id} в Меню Id:{menu_id} обнавлена'

        # удаление записи подменю
        async def submenu_delete_record(self, menu_id: int, submenus_id: int):
            engine = await db.async_connect()

            async with engine.begin() as conn:

                await conn.execute(dishes.delete().where(
                    dishes.c.menu_id == menu_id, dishes.c.sub_menu_id == submenus_id))
                await conn.execute(sub_menus.delete().where(
                    sub_menus.c.menu_id == menu_id, sub_menus.c.sub_menu_id == submenus_id))

                await engine.dispose()
                return f'Запись Подменю Id:{submenus_id} удалена из Меню Id:{menu_id}'

    # Интерфейс блюд
    class _DishesInteface:

        # конструктор блюда
        def __init__(self, title=None, description=None, price=None):
            self.title = title
            self.description = description
            self.price = price

        # получение блюда по Id или все
        async def dish_get(self, menu_id: int, submenus_id: int, dishes_id=None):
            engine = await db.async_connect()
            result = []

            async with engine.begin() as conn:

                if dishes_id is None:
                    request = await conn.execute(dishes.select().where(
                        dishes.c.menu_id == menu_id, dishes.c.sub_menu_id == submenus_id))
                    for row in request:
                        dish_list = {}

                        dish_list['id'] = row[0]
                        dish_list['sub_menu_id'] = str(row[1])
                        dish_list['menu_id'] = str(row[2])
                        dish_list['title'] = row[3]
                        dish_list['description'] = row[4]
                        dish_list['price'] = '%.2f' % row[5]

                        result.append(dish_list)
                else:
                    cache = await redis_cache._DishMemCache().cache_get_dish(dishes_id, submenus_id, menu_id)
                    if cache:
                        return JSONResponse(content=cache, status_code=200)

                    request = await conn.execute(dishes.select().where(
                        dishes.c.menu_id == menu_id, dishes.c.sub_menu_id == submenus_id, dishes.c.dish_id == dishes_id))
                    for row in request:
                        dish_list = {}

                        dish_list['id'] = str(row[0])
                        dish_list['sub_menu_id'] = str(row[1])
                        dish_list['menu_id'] = str(row[2])
                        dish_list['title'] = row[3]
                        dish_list['description'] = row[4]
                        dish_list['price'] = '%.2f' % row[5]

                        await redis_cache._DishMemCache().cache_set_dish(
                            dishes_id, submenus_id, menu_id, dish_list)
                        return JSONResponse(content=dish_list, status_code=200)

                if result:
                    await engine.dispose()
                    return JSONResponse(content=result, status_code=200)
                elif dishes_id:
                    await engine.dispose()
                    response = {}
                    response['detail'] = 'dish not found'
                    return JSONResponse(content=response, status_code=404)
                else:
                    await engine.dispose()
                    return JSONResponse(content=[], status_code=200)

        # Добавления нового блюда
        async def dish_add_record(self, menu_id: int, submenus_id: int):
            engine = await db.async_connect()

            async with engine.begin() as conn:

                request = await conn.execute(select(sub_menus).where(
                    sub_menus.c.menu_id == menu_id, sub_menus.c.sub_menu_id == submenus_id))
                if not request.fetchall():
                    return JSONResponse(content='Нету такого подменю и меню', status_code=200)

                request = await conn.execute(dishes.select().where(
                    dishes.c.menu_id == menu_id))

                for row in request:
                    if self.title == row[3]:
                        print(row[3])
                        return JSONResponse(content=f'Блюдо с названием {self.title} уже присутствует в Подменю Id{submenus_id}', status_code=201)

                request = await conn.execute(dishes.insert().values(sub_menu_id=submenus_id, menu_id=menu_id,
                                                                    title=self.title, description=self.description, price=self.price))

                req = await conn.execute(dishes.select().where(dishes.c.sub_menu_id == submenus_id, dishes.c.menu_id == menu_id,
                                                               dishes.c.title == self.title, dishes.c.description == self.description, dishes.c.price == self.price))
                request = req.fetchall()

                response = {
                    'id': str(request[0][0]),
                    'sub_menu_id': request[0][1],
                    'menu_id': request[0][2],
                    'title': request[0][3],
                    'description': request[0][4],
                    'price': str(request[0][5])
                }

                await redis_cache._DishMemCache().cache_set_dish(
                    request[0][0], request[0][1], request[0][2], response)

                await engine.dispose()
                return JSONResponse(content=response, status_code=201)

        # Обновление записи
        async def dish_update_record(self, menu_id: int, submenus_id: int, dishes_id: int):
            engine = await db.async_connect()

            async with engine.begin() as conn:

                request = await conn.execute(dishes.select().where(dishes.c.menu_id == menu_id,
                                                                   dishes.c.sub_menu_id == submenus_id, dishes.c.dish_id == dishes_id))
                if not request.fetchall():
                    return f'Не найдено Блюдо Id:{dishes_id} в Подменю Id:{submenus_id} в Меню по Id:{menu_id}'

                print(f'PRICE {self.price}')

                request = await conn.execute(dishes.update().where(sub_menus.c.menu_id == menu_id, sub_menus.c.sub_menu_id ==
                                                                   submenus_id, dishes.c.dish_id == dishes_id).values(title=self.title, description=self.description, price=self.price))

                await redis_cache._DishMemCache().cache_update_dish(dishes_id, submenus_id,
                                                                    menu_id, self.title, self.description, self.price)

                await engine.dispose()

                return f'Обновлено Блюдо Id:{dishes_id} в Подменю Id:{submenus_id} в Меню по Id:{menu_id}'

        # Удаление записи
        async def dish_delete_record(self, menu_id: int, submenus_id: int, dishes_id: int):
            engine = await db.async_connect()

            async with engine.begin() as conn:

                request = await conn.execute(dishes.delete().where(
                    dishes.c.menu_id == menu_id, dishes.c.sub_menu_id == submenus_id, dishes.c.dish_id == dishes_id))

                await redis_cache._DishMemCache().cache_del_dish(dishes_id, submenus_id, menu_id)

                await engine.dispose()
                return f'Запись блюда Id:{dishes_id} успешно удалена из Меню Id:{menu_id}, Подменю Id:{submenus_id}'

    class _SpecialRequest:

        async def get_all_records(self):
            engine = await db.async_connect()

            async with engine.begin() as conn:
                resp = []

                request = select(sub_menus, dishes).join(
                    dishes, dishes.c.sub_menu_id == sub_menus.c.sub_menu_id)

                subq = request.subquery()

                req = select(menus, subq).join(
                    subq, subq.c.menu_id == menus.c.menu_id)

                response = await conn.execute(req)

                for row in response:
                    r = {
                        'id': row[0],
                        'title': row[1],
                        'description': row[2],
                        'sub_menus': {
                            'id': row[3],
                            'menu_id': row[4],
                            'title': row[5],
                            'description': row[6],
                            'dish:': {
                                'id': row[7],
                                'submenu_id': row[8],
                                'menu_id': row[9],
                                'title': row[10],
                                'description': row[11],
                                'price': row[12]
                            }
                        }
                    }
                    resp.append(r)

                return JSONResponse(content=resp, status_code=200)
