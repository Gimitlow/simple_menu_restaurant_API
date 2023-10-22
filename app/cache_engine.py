import redis
import json
import os

#подключение редиса
host = os.environ.get('REDIS_HOST')
port = os.environ.get('REDIS_PORT')
redis_cache = redis.Redis(host=host, port=port, db=0)

class RedisMemCache:

	class _MenuMemCache:

		def cache_get_menu(self, id: str):
			cache = redis_cache.get(f'Menu-{id}')
			if cache:
				print(f'Menu {id} cache found.')
				redis_cache.close()
				return json.loads(cache)
			else:
				print(f'No menu {id} cache found.')
				redis_cache.close()

		def cache_set_menu(self, id: str, data):
			cache = redis_cache.set(f'Menu-{id}', json.dumps(data))
			print(f'Set menu {id} cache.')
			redis_cache.close()

		def cache_update_menu(self, id: str, title: str, description: str):
			cache = json.loads(redis_cache.get(f'Menu-{id}'))
			if cache:
				cache['title'] = title
				cache['description'] = description
				redis_cache.set(f'Menu-{id}', json.dumps(cache))
				redis_cache.close()
				print(f'Menu {id} cache updated.')

		def cache_del_menu(self, id: str):
			cache = redis_cache.get(f'Menu-{id}')
			if cache:
				redis_cache.delete(f'Menu-{id}')
				print(f'Menu {id} delete from cache.')

	class _SubmenuMemCache:

		def cache_get_submenu(self, submenu_id: str, menu_id: str):
			cache = redis_cache.get(f'Menu-{menu_id}-Submenu-{submenu_id}')
			if cache:
				print(f'Submenu {submenu_id} from Menu {menu_id} cache found.')
				redis_cache.close()
				return json.loads(cache)
			else:
				print(f'No submenu {submenu_id} cache {menu_id} found.')
				redis_cache.close()

		def cache_set_submenu(self, submenu_id: str, menu_id: str, data):
			cache = redis_cache.set(f'Menu-{menu_id}-Submenu-{submenu_id}', json.dumps(data))
			print(f'Set Submenu {submenu_id} from Menu {menu_id} cache.')
			redis_cache.close()

		def cache_update_submenu(self, submenu_id: str, menu_id: str, title: str, description: str):
			cache = json.loads(redis_cache.get(f'Menu-{menu_id}-Submenu-{submenu_id}'))
			if cache:
				cache['title'] = title
				cache['description'] = description
				redis_cache.set(f'Menu-{menu_id}-Submenu-{submenu_id}', json.dumps(cache))
				redis_cache.close()
				print(f'Submenu {submenu_id} from Menu {menu_id} cache updated.')

		def cache_del_submenu(self, submenu_id: str, menu_id: str):
			cache = redis_cache.get(f'Menu-{menu_id}-Submenu-{submenu_id}')
			if cache:
				redis_cache.delete(f'Menu-{menu_id}-Submenu-{submenu_id}')
				print(f'Submenu {submenu_id} from Menu {menu_id} delete from cache.')

	class _DishMemCache:

		def cache_get_dish(self, dish_id: str, submenu_id: str, menu_id: str):
			cache = redis_cache.get(f'Menu-{menu_id}-Submenu-{submenu_id}-Dish-{dish_id}')
			if cache:
				print(f'Dish {dish_id} from Submenu {submenu_id} from Menu {menu_id} cache found.')
				redis_cache.close()
				return json.loads(cache)
			else:
				print(f'No Dish {dish_id} from Submenu {submenu_id} from Menu {menu_id} cache found.')

		def cache_set_dish(self, dish_id: str, submenu_id: str, menu_id: str, data):
			cache = redis_cache.set(f'Menu-{menu_id}-Submenu-{submenu_id}-Dish-{dish_id}', json.dumps(data))
			print(f'Set Dish {dish_id} from Submenu {submenu_id} from Menu {menu_id} cache.')
			redis_cache.close()

		def cache_update_dish(self, dish_id: str, submenu_id: str, menu_id: str, title: str, description: str, price: str):
			cache = json.loads(redis_cache.get(f'Menu-{menu_id}-Submenu-{submenu_id}-Dish-{dish_id}'))
			if cache:
				cache['title'] = title
				cache['description'] = description
				cache['price'] = "%.2f" % price
				redis_cache.set(f'Menu-{menu_id}-Submenu-{submenu_id}-Dish-{dish_id}', json.dumps(cache))
				redis_cache.close()
				print(f'Dish {dish_id} from Submenu {submenu_id} from Menu {menu_id} cache updated.')

		def cache_del_dish(self, dish_id: str, submenu_id: str, menu_id: str):
			cache = redis_cache.get(f'Menu-{menu_id}-Submenu-{submenu_id}-Dish-{dish_id}')
			if cache:
				redis_cache.delete(f'Menu-{menu_id}-Submenu-{submenu_id}-Dish-{dish_id}')
				print(f'Dish {dish_id} from Submenu {submenu_id} from Menu {menu_id} delete from cache.')