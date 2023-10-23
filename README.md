# simple_menu_restaurant_API
Простое API для меню ресторана. Учебный проект

# Технологии, которые используются
Python (FastAPI, sqlalchemy)<br/>
PostgreSQL, Redis<br/>
Docker

# История изменений:
v1.0.1 - добавлена логика работы меню<br/>
v1.0.2 - добавлена логика работы с подменю, мелкие правки прошлой версии<br/>
v1.1.0 LTS - добавлена вся окончательная логика, работа с меню, подменю, блюдами(позициями)<br/>
v1.1.1 LTS - багфикс<br/>
v1.1.2 LTS - багфикс<br/>
v2.2.0 LTS - добавлена поддержка Docker, включены тесты<br/>
v3.0.0 LTS - добавлено кэширование запросов Redis<br/>
v3.0.1 LTS - добавлен pre-commit<br/>
v3.0.1 LTS - API переведен в асинхронное приложение<br/>


# Как запустить?
1) Скачиваем проект через git<br/>
`git clone https://github.com/Gimitlow/simple_menu_restaurant_API.git`<br/>
2) Собираем проект<br/>
`docker-compose build`<br/>
3) Запускаем проект<br/>
`docker-compose up -d`<br/>
4) Проект запуститься на http://0.0.0.0:8000/

# Запуск тестов
- После сборки и запуска пишем команду<br/>
`docker-compose run test`<br/>

# Проверка кода <br/>
- Перед сборкой можно запустить хук проверки<br/>
`pre-commit run --all-files`<br/>
