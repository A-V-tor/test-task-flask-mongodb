import json
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import use_kwargs, doc
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

# локальный запуск mongodb
# client = MongoClient('localhost', 27017)

# запуск mongodb через докер
client = MongoClient(host='test_mongodb')

docs = FlaskApiSpec(app)

db = client.flask_db
todos = db.users


app.config.update(
    {
        'APISPEC_SPEC': APISpec(
            title='document-api',
            version='v1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        )
    }
)


@app.route('/', methods=('GET', 'POST'))
def index():
    """Визуальное отображение состояния бд"""

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['psw']
        todos.insert_one({'name': name, 'password': password})
        return redirect(url_for('index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.post('/<id>/delete/')
def delete(id):
    """Удаление пользователя из бд, со страницы

    визуального отображения состояния бд"""

    todos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


# _____________________маршруты для API_____________________


class UsersSchema(Schema):
    name = fields.String(required=True)
    psw = fields.String(required=True)


@docs.register
@doc(description='Запрос всех пользователей')
@app.get('/users')
def get_all_users():
    """Возврат всего списка пользователей"""

    try:
        all_users = todos.find()
        return json.loads(dumps(all_users, ensure_ascii=False))

    except Exception as e:
        return jsonify({'error': str(e)})


@docs.register
@doc(description='Запрос на добавление нового пользователя')
@use_kwargs(UsersSchema, location='json')
@app.post('/add-user')
def add_user():
    """Добавление пользователя в бд"""

    try:
        data = request.get_json()
        name = data['name']
        password = data['psw']
        todos.insert_one({'name': name, 'password': password})
        return jsonify({'success': 'user added'})

    except Exception as e:
        return jsonify({'error': str(e)})


@docs.register
@doc(description='Запрос на удаление пользователя')
@app.delete('/delete/<id>/')
def delete_id(id):
    """Удаление пользователя из бд"""

    try:
        if entries := todos.find_one({'_id': ObjectId(id)}):
            todos.delete_one(entries)
            return json.loads(dumps(entries, ensure_ascii=False))

        return jsonify({'no data with this id': id})
    except Exception as e:
        return jsonify({'error': str(e)})
