# Тестовое задание для Ришат
## Проект для знакомства с Stripe

### Зависимости
- docker
- docker-compose
- stripe cli

### Установка и настройка
- sudo docker-compose up --build
- stripe listen --forward-to localhost:8000/webhook/stripe/
- sudo docker-compose exec web python manage.py migrate
- sudo docker-compose exec web python manage.py createsuperuser  

### Доп пункты тз:
- Запуск используя Docker +
- Использование environment variables +
- Просмотр Django Моделей в Django Admin панели +
- Запуск приложения на удаленном сервере, доступном для тестирования -
- Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items +
- Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe + 
- Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте - (не понятно как должно работать в сочетании с Order)
- Реализовать не Stripe Session, а Stripe Payment Intent. +

Для удобства тестирования реализованы каталог, страница тавара и карзина на основе сессий

Над дезайном не сильно запаривался, всё таки я backend разраб и времени на продумывание дизайна не особо много