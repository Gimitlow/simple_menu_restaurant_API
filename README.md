# simple_menu_restaurant_API
Простое API для меню ресторана. Учебный проект

# Технологии, которые используются
Python (FastAPI, sqlalchemy)<br/>
PostgreSQL, Redis<br/>
Celery+RabbitMQ<br/>
Docker

# Как запустить?
1) Скачиваем проект через git<br/>
`git clone https://github.com/Gimitlow/simple_menu_restaurant_API.git`<br/>
2) Собираем проект<br/>
`docker-compose build`<br/>
3) Запускаем проект<br/>
`docker-compose up -d`<br/>
4) Проект запуститься на http://0.0.0.0:8000/<br/>

# Запуск админки<br/>
- После того как проект запуститься, можно активировать админу xlsx /console <br/>

# Запуск тестов
- После сборки и запуска пишем команду<br/>
`docker-compose run test`<br/>

# Вспомогательные инструменты<br/>
- Админка PostgreSQL - http://127.0.0.1:5011/
- Админка RabbitMQ - http://127.0.0.1:15672/

# Проверка кода <br/>
- Перед сборкой можно запустить хук проверки<br/>
`pre-commit run --all-files`<br/>
