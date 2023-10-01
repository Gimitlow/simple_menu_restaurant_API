# simple_menu_restaurant_API
Простое API для меню ресторана. Учебный проект

# Технологии, которые используются
Python (FastAPI, sqlalchemy)
PostgreSQL

# История изменений: 
v1.0.1 - добавлена логика работы меню
v1.0.2 - добавлена логика работы с подменю, мелкие правки прошлой версии

# Как запустить?
1) Скачиваем проект через git
`git clone https://github.com/Gimitlow/simple_menu_restaurant_API.git`
2) Запускаем окружение в папке /myenv/Scripts через `cmd`
`C:\Users\Gleb>active.bat`
3) Выходим в корневой каталог `simple_menu_restaurant_API` посредством `cmd` `cd ..`
4) Запускаем uvicorn командой 
`unicorn main:app --reload`
5) Запускаем PostgreSQL и создаем там БД, можно скачать pgAdmin4
6) В файле конфигурацаии БД `db_config.py` указываем логопасы для подключения
`
	login = 'postgres' #логин 
	password = 'admin' #пароль
	host = 'localhost' #по умолчанию локальный адрес
	db_name = 'restaurant_api' #имя базы, которую создали ранее
`
