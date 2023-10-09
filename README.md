# simple_menu_restaurant_API
Простое API для меню ресторана. Учебный проект

# Технологии, которые используются
Python (FastAPI, sqlalchemy)<br/>
PostgreSQL

# История изменений: 
v1.0.1 - добавлена логика работы меню<br/>
v1.0.2 - добавлена логика работы с подменю, мелкие правки прошлой версии<br/>
v1.1.0 LTS - добавлена вся окончательная логика, работа с меню, подменю, блюдами(позициями)<br/>
v1.1.1 LTS - багфикс<br/>
v1.1.2 LTS - багфикс


# Как запустить?
1) Скачиваем проект через git<br/>
`git clone https://github.com/Gimitlow/simple_menu_restaurant_API.git`
2) Запускаем окружение в папке /myenv/Scripts через `cmd`<br/>
`C:\Users\Gleb>active.bat`
3) Выходим в корневой каталог `simple_menu_restaurant_API` посредством `cmd` `cd ..`
4) Запускаем uvicorn командой<br/>
`unicorn main:app --reload`
5) Запускаем PostgreSQL и создаем там БД, можно скачать pgAdmin4
6) В файле конфигурацаии БД `db_config.py` указываем логопасы для подключения<br/>
`
	login = 'postgres' #логин 
	password = 'admin' #пароль
	host = 'localhost' #по умолчанию локальный адрес
	db_name = 'restaurant_api' #имя базы, которую создали ранее
`
