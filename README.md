# Задание для Back-end разработчиков

**Задание:**

- создать сервер на Flask (для Python) или Express (если NodeJS),

- подключить базу данных (mongo DB),

- создать пользователя в базе данных,

- проверить как работает, через Postman

Подключаться к API не требуется, мокайте данные.

<h1 align="center">Развертывание проекта</h1>

<h2>Скачать проект</h2>

```
  git@github.com:A-V-tor/test-task-flask-mongodb.git
  cd test-task-flask-mongodb
```

<h3>1. Запуск через docker</h3>

```
  docker-compose up
```

<h3>2. Запуск локальной версии</h3>

<i>В файле init перекомментить строки</i>

```
  # локальный запуск mongodb
  client = MongoClient('localhost', 27017)

  # запуск mongodb через докер
  # client = MongoClient(host='test_mongodb')

```
<i>Пример запуска mongodb через brew</i>

```
  brew services start mongodb-community@6.0
  gunicorn -w 3 -b 0.0.0.0:5000 app:app 
```

<h3>3. Url адресса</h3>

<p>Главная страница</p>

```
  http://127.0.0.1:5000  
```

или

```
  http://0.0.0.0:5000
```

<p>Документация</p>

```
  http://127.0.0.1:5000/swagger-ui 
```

или

```
  http://0.0.0.0:5000/swagger-ui/
```

<img src="https://github.com/A-V-tor/test-task-flask-mongodb/blob/main/documentation.png">
