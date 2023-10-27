import requests
import json
import os
from time import sleep

# глобальные переменные
host = os.environ.get('APP_URL')
url = f'http://{host}:8000/'

# инетрфейс для обновления информации


class AdminInterface:

    def menu_data(self, id: str, title: str, description: str):

        menus = {
            'title': title,
            'description': description
        }

        req = requests.get(f'{url}api/v1/menus/{id}').json()

        if 'detail' in req:
            r = requests.post(f'{url}api/v1/menus', json=menus)
        else:
            r = requests.patch(f'{url}api/v1/menus/{id}', json=menus)

    def submenu_data(self, id: str, menu_id: str, title: str, description: str):

        submenus = {
            'title': title,
            'description': description
        }

        req = requests.get(f'{url}api/v1/menus/{menu_id}/submenus/{id}').json()

        if 'detail' in req:
            r = requests.post(f'{url}api/v1/menus/{menu_id}/submenus', json=submenus)
        else:
            r = requests.patch(f'{url}api/v1/menus/{menu_id}/submenus/{id}', json=submenus)

    def dish_data(self, menu_id: str, submenu_id: str, id: str, title: str, description: str, price: str):

        dishes = {
            'title': title,
            'description': description,
            'price': '%.2f' % price
        }

        req = requests.get(f'{url}api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}').json()

        if 'detail' in req:
            print(f'[ADMIN] SET ({url}) {menu_id} {submenu_id} {id} {title} {description} {price}')
            r = requests.post(f'{url}api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dishes)
        else:
            print(f'[ADMIN] UPDATE ({url}) {menu_id} {submenu_id} {id} {title} {description} {price}')
            r = requests.patch(f'{url}api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}', json=dishes)
