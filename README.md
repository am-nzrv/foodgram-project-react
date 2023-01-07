# Продуктовый помощник (дипломный проект)


## Описание:
 Проект "**Продуктовый помощник**" это онлайн-сервис на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Запуск проекта в dev-режиме (доступна админка и api, без фронта)
```
    python -m venv venv
    source venv/Scripts/activate (venv/bin/activate)
    cd backend/
    pip install -r requirements.txt
```
#### Наполнение env-файла для dev-режима:

```
    echo '''SECRET_KEY=super-key
    DEBUG=True
    DB_ENGINE=django.db.backends.sqlite3
    DB_NAME=db.sqlite3
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    DB_HOST=
    DB_PORT=
    ''' > .env
```

#### Запуск

```
python manage.py migrate
python manage.py createsuperuser
python manage.py load_tags_data
python manage.py load_ingredients_data
python manage.py runserver
```

## Запуск проект в контейнерах:

                                     It's done when it's done

Но потом, проект будет доступен по адресу: [http://51.250.107.160/](http://51.250.107.160/)

DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

