# Здесь будет описание проекта SuperStore.
[Демка сайта - SuperSore](https://notfounduser404.pythonanywhere.com/).

## Коротко: 
### Тестовый интернет-магазин на Django с авторизацией, корзиной, оплатой через Stripe Pyayment Element и созданием заказа после успешной опалты.

## Возможности:
* Каталог, карточка товара, корзина, оформление заказа.
* Аторизация/регистрация
* Корзина только для авторизованных пользователей
* Оплата через Stripe PaymentIntent
* Создание Order/OrderItem после успешной оплаты

## Быстрый старт в Docker (Compose)
1. Требования
    Docker и Docker Compose v2 (docker compose version)
2. Подготовка env для Docker
    оздайте фалй .env.compose в корне (рядом с docker-compose.yml) по примеру .env.compose.example.
3. Запуск
    Первый запуск (с чистым томом БД): docker compose down -v docker compose up --build
    Открыть: http://localhost:8000


## Локальный запуск без Docker (опционально)

1. Устновить зависимовти

       python -m venv venv
       source venv/bin/activate
       pip install -r requirements.txt

3. Подготовка .env
    Создайте файл .env в корне по примеру .env.example

4. Создайте суперпользователя, чтобы добавлять товары через админку.

       python manage.py migrate
       python manage.py createsuperuser
6. Запуск

       python manage.py runserver
