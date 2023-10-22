import os

import params
import pytest
import requests

address = os.environ.get('APP_URL')
base_url = f'http://{address}:8000/api/v1'

# MENUS


@pytest.mark.menu
def test_get_all_menus():
    response = requests.get(f'{base_url}/menus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.menu
def test_create_menu():
    response = requests.post(f'{base_url}/menus', json=params.params_menu_create)
    params.menu_id = response.json()['id']
    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['title'] in params.params_menu_create['title']
    assert response.json()[
        'description'] in params.params_menu_create['description']


@pytest.mark.menu
def test_get_all_menus_2():
    response = requests.get(f'{base_url}/menus')
    assert response.status_code == 200
    assert response.json() != []
    for row in response.json():
        assert row['id'] and row['title'] and row['description'] and row['submenus_count'] != [
        ] and row['dishes_count'] != []


@pytest.mark.menu
def test_get_target_menu():
    response = requests.get(f'{base_url}/menus/{params.menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] and response.json()['title'] and response.json()[
        'submenus_count'] != [] and response.json()['dishes_count'] != []


@pytest.mark.menu
def test_update_target_menu():
    response = requests.patch(f'{base_url}/menus/{params.menu_id}', json=params.params_menu_update)
    assert response.status_code == 200
    response = requests.get(f'{base_url}/menus/{params.menu_id}')
    assert response.status_code == 200
    assert response.json()['title'] == params.params_menu_update['title'] and response.json()[
        'description'] == params.params_menu_update['description']


@pytest.mark.menu
def test_get_target_menu_2():
    response = requests.get(f'{base_url}/menus/{params.menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] and response.json()['title'] and response.json()[
        'submenus_count'] != [] and response.json()['dishes_count'] != []


@pytest.mark.menu
def test_delete_target_menu():
    response = requests.delete(f'{base_url}/menus/{params.menu_id}')
    assert response.status_code == 200


@pytest.mark.menu
def test_get_all_menus_3():
    response = requests.get(f'{base_url}/menus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.menu
def test_get_target_menu_3():
    response = requests.get(f'{base_url}/menus/{params.menu_id}')
    assert response.status_code == 404
    assert response.json() == params.params_menu_not_found

# SUBMENUS


@pytest.mark.submenu
def test_sumbmenu_create_menu():
    response = requests.post(f'{base_url}/menus', json=params.params_menu_create)
    params.menu_id = response.json()['id']
    assert response.status_code == 201
    assert response.json()['id']


@pytest.mark.submenu
def test_submenu_get_all_submenus():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.submenu
def test_submenu_create():
    response = requests.post(f'{base_url}/menus/{params.menu_id}/submenus', json=params.params_submenu_create)
    assert response.status_code == 201
    params.submenu_id = response.json()['id']
    assert response.json()['id']
    assert response.json()['menu_id']
    assert response.json()['title'] == params.params_submenu_create['title']
    assert response.json()[
        'description'] == params.params_submenu_create['description']
    assert response.json()['dish_count'] != []


@pytest.mark.submenu
def test_submenu_get_all_submenus_2():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus')
    assert response.status_code == 200
    for row in response.json():
        assert row['id'] and row['menu_id'] and row['title'] and row['description'] and row['dishes_count'] != []


@pytest.mark.submenu
def test_submenu_get_target():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}')
    assert response.json()['id'] != [] and response.json()['menu_id'] != [] and response.json()[
        'title'] != [] and response.json()['description'] != [] and response.json()['dishes_count'] != []


@pytest.mark.submenu
def test_submenu_update():
    response = requests.patch(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}',
                              json=params.params_submenu_update)
    assert response.status_code == 200
    req = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}')
    assert req.json()['id'] != [] and req.json()['menu_id'] != [] and req.json()['title'] == params.params_submenu_update['title'] and req.json()[
        'description'] == params.params_submenu_update['description'] and req.json()['dishes_count'] != []


@pytest.mark.submenu
def test_submenu_get_target_2():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}')
    assert response.json()['id'] != [] and response.json()['menu_id'] != [] and response.json()[
        'title'] != [] and response.json()['description'] != [] and response.json()['dishes_count'] != []


@pytest.mark.submenu
def test_delete_target_submenu():
    response = requests.delete(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}')
    assert response.status_code == 200


@pytest.mark.submenu
def test_submenu_get_all_submenus_3():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.submenu
def test_submenu_get_target_3():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}')
    assert response.status_code == 404
    assert response.json() == params.params_submenu_not_found


@pytest.mark.submenu
def test_submenu_delete_menu():
    response = requests.delete(f'{base_url}/menus/{params.menu_id}')
    assert response.status_code == 200


@pytest.mark.submenu
def test_submenu_get_all_menus():
    response = requests.get(f'{base_url}/menus')
    assert response.status_code == 200
    assert response.json() == []

# DISHES


@pytest.mark.dish
def test_dish_create_menu():
    response = requests.post(f'{base_url}/menus', json=params.params_menu_create)
    params.menu_id = response.json()['id']
    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['title'] in params.params_menu_create['title']
    assert response.json()[
        'description'] in params.params_menu_create['description']


@pytest.mark.dish
def test_dish_submenu_create():
    response = requests.post(f'{base_url}/menus/{params.menu_id}/submenus', json=params.params_submenu_create)
    assert response.status_code == 201
    params.submenu_id = response.json()['id']
    assert response.json()['id']
    assert response.json()['menu_id']
    assert response.json()['title'] == params.params_submenu_create['title']
    assert response.json()[
        'description'] == params.params_submenu_create['description']
    assert response.json()['dish_count'] != []


@pytest.mark.dish
def test_dish_get_all():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.dish
def test_dish_create():
    response = requests.post(
        f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes', json=params.params_dish_create)
    assert response.status_code == 201
    params.dish_id = response.json()['id']
    assert response.json()['id'] and response.json()[
        'sub_menu_id'] and response.json()['menu_id']
    assert response.json()['title'] == params.params_dish_create['title']
    assert response.json()[
        'description'] == params.params_dish_create['description']
    assert float(response.json()['price']) == float(
        params.params_dish_create['price'])


@pytest.mark.dish
def test_dish_get_all_2():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.dish
def test_dish_get_target():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes/{params.dish_id}')
    assert response.status_code == 200
    assert response.json()['id']
    assert response.json()['sub_menu_id']
    assert response.json()['menu_id']
    assert response.json()['title']
    assert response.json()['description']
    assert response.json()['price']


@pytest.mark.dish
def test_dish_update():
    response = requests.patch(
        f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes/{params.dish_id}', json=params.params_dish_update)
    assert response.status_code == 200
    req = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes/{params.dish_id}')
    assert req.json()['title'] in params.params_dish_update['title'] and req.json()[
        'description'] in params.params_dish_update['description'] and req.json()['price'] == params.params_dish_update['price']


@pytest.mark.dish
def test_dish_get_target_2():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes/{params.dish_id}')
    assert response.status_code == 200
    assert response.json()['id']
    assert response.json()['sub_menu_id']
    assert response.json()['menu_id']
    assert response.json()['title']
    assert response.json()['description']
    assert response.json()['price']


@pytest.mark.dish
def test_dish_delete():
    response = requests.delete(
        f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes/{params.dish_id}')
    assert response.status_code == 200


@pytest.mark.dish
def test_dish_get_all_3():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.dish
def test_dish_get_target_4():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}/dishes/{params.dish_id}')
    assert response.status_code == 404
    assert response.json()['detail'] == params.params_dish_not_found['detail']


@pytest.mark.dish
def test_dish_delete_submenu():
    response = requests.delete(f'{base_url}/menus/{params.menu_id}/submenus/{params.submenu_id}')
    assert response.status_code == 200


@pytest.mark.dish
def test_dish_get_all_submenus():
    response = requests.get(f'{base_url}/menus/{params.menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.dish
def test_dish_delete_menu():
    response = requests.delete(f'{base_url}/menus/{params.menu_id}')
    assert response.status_code == 200


@pytest.mark.dish
def test_dish_get_all_menus():
    response = requests.get(f'{base_url}/menus')
    assert response.status_code == 200
    assert response.json() == []
