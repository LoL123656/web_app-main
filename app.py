from flask import Flask, request, render_template
import sqlite3  
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

# Определение формы для добавления фильма
class MyForm(FlaskForm):
    # Поле для названия фильма
    name = StringField('Название', validators=[DataRequired()]) 
    # Поле для года выпуска фильма
    year = IntegerField('Год выпуска')
    # Поле для рейтинга фильма
    rating = FloatField('Рейтинг')
    # Поле для жанра фильма
    genre = StringField('Жанр')

# Инициализация Flask приложения
app = Flask(__name__)

# Настройка соединения с базой данных (sqlite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.db'
db = SQLAlchemy(app)

# Модель фильма для SQLAlchemy
class Film(db.Model):
    __tablename__ = 'Movies'  # Указываем название таблицы

    # Определяем столбцы таблицы
    id = db.Column(db.Integer, primary_key=True)  # ID фильма (первичный ключ)
    name = db.Column(db.String(80))  # Название фильма
    year = db.Column(db.Integer)  # Год выпуска фильма
    rating = db.Column(db.Float)  # Рейтинг фильма
    genre = db.Column(db.String(80))  # Жанр фильма

    # Конструктор для создания нового объекта Film
    def __init__(self, name, year, rating, genre):
        self.name = name
        self.year = year
        self.rating = rating
        self.genre = genre

# Создание соединения с базой данных  
con = sqlite3.connect('./instance/films.db', check_same_thread=False)
# Создание курсора для выполнения SQL запросов  
cur = con.cursor()

# Маршрут для корневой страницы
@app.route("/")
def hello_world():
    # Возвращение приветственного сообщения
    return render_template('main.html')

# Маршрут для получения информации о фильме по ID
@app.route("/film/<id>")
def film(id):
    # Выполнение SQL запроса для получения данных о фильме по ID
    #res = cur.execute(f"select * from Movies where id = ?", (id,))
    # Получение результата запроса
    #film = res.fetchone()
    #print(film)
    film = Film.query.filter_by(id=id).all()
    print(film)
    # Проверка, найден ли фильм
    if film != []:
        # Возвращение результата
        return render_template('film.html', film = film[0] )
    else:
        # Сообщение о том, что фильма не существует   
        return "Такого фильма нет"

# Маршрут для получения списка всех фильмов
@app.route("/films" )
def films():
    # Выполнение SQL запроса для получения всех фильмов
    #res = cur.execute("select * from Movies")
    # Получение результата запроса
    #films = res.fetchall()
    films = Film.query.all()
    # Возвращение списка фильмов
    return render_template('films.html', films = films)

# Маршрут для отображения формы добавления фильма
@app.route("/film_form", methods=['GET', 'POST'])
def film_form():
    # Создание формы
    form = MyForm()
    # Проверка, была ли отправлена заполненная форма на сервер
    if form.validate_on_submit():
        # Извлекаем данные из формы
        name=form.data['name']
        year=form.data['year']
        rating=form.data['rating']
        genre=form.data['genre']
        #Создаем объект фильма
        new_film = Film(name, genre, year, rating)
        #Добавляем в БД
        db.session.add(new_film)
        #Фиксируем изменения
        db.session.commit()
        # ниже вариант с использованием sqlite3
        # film_data = (name, genre, year, rating)
        # # Выполнение SQL запроса для добавления фильма в базу данных
        # cur.execute('INSERT INTO Movies (name, genre, year, rating) VALUES (?, ?, ?, ?)', film_data)
        # # Сохранение изменений в базе данных
        # con.commit()
        return 'Фильм добавлен!'
    # Возвращаем форму для отображения к заполнению
    return render_template('form.html', form=form)

#Маршрут для добавления нового фильма
@app.route("/film_add")
def film_add():
    # Получение данных о фильме из параметров запроса
    name = request.args.get('name')
    genre = request.args.get('genre')
    year = request.args.get('year')
    rating = request.args.get('rating')
    # Формирование кортежа с данными о фильме
    film_data = (name, genre, year, rating)
    # Выполнение SQL запроса для добавления фильма в базу данных
    cur.execute('INSERT INTO Movies (name, genre, year, rating) VALUES (?, ?, ?, ?)', film_data)
    # Сохранение изменений в базе данных
    con.commit()
    # Возвращение подтверждения о добавлении фильма
    return "name = {};genre = {}; year = {}; rating = {} ".format(name, genre, year, rating) 

# Запуск приложения, если оно выполняется как главный модуль
if __name__ == '__main__':
    # Отключение проверки CSRF для WTForms
    app.config["WTF_CSRF_ENABLED"] = False  
    # Запуск приложения в режиме отладки
    app.run(debug=True)
