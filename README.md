# Продуктовый помощник (дипломный проект)




## Описание:
 Проект "**Продуктовый помощник**" это онлайн-сервис на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.





## Запуск проекта в dev-режиме (доступна админка и api, без фронта, БД - SQLite)

#### Установка окружения и зависимостей.

>     python -m venv venv 
> 
>     source venv/Scripts/activate (venv/bin/activate)
> 
>     cd backend/ pip install -r requirements.txt

#### Создадим env-файл для dev-режима:

>     echo '''DB_ENGINE=django.db.backends.sqlite3
>     DB_NAME=db.sqlite3
>     POSTGRES_USER=
>     POSTGRES_PASSWORD=
>     DB_HOST=
>     DB_PORT=
>     enter code here''' > .env

#### Запуск

>     python manage.py makemigrations
>     python manage.py migrate
>     python manage.py createsuperuser
>     python manage.py load_tags_data
>     python manage.py load_ingredients_data
>     python manage.py runserver


## Запуск проект в контейнерах:
#### Переходим в директорию infra
                      
>     cd foodgram-project-react/infra/

#### Cоздадим env-файл для запуска в контейнерах:

>     echo '''DB_ENGINE=django.db.backends.postgresql  
>     DB_NAME=postgres  
>     POSTGRES_USER=postgres  
>     POSTGRES_PASSWORD=postgres  
>     DB_HOST=db   
>     DB_PORT=5432  
>     ''' > .env

#### Запуск

>     docker-compose up -d --build
>     docker-compose exec backend python manage.py makemigrations
>     docker-compose exec backend python manage.py migrate
>     docker-compose exec backend python manage.py collectstatic --no-input
>     docker-compose exec backend python manage.py createsuperuser
>     docker-compose exec backend python manage.py load_tags_data
>     docker-compose exec backend python manage.py load_ingredients_data


## Деплой на сервере Яндекс.Облака                         

Пока в работе

