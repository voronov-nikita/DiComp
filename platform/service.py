from flask import Flask, render_template, session, redirect, url_for, request
from database import *
import secrets


# константные данные для порта и имени хоста на котором хостится приложение
PORT: int = 8080
HOST: str = "localhost"


app = Flask(__name__)
key = secrets.token_hex(16)
app.secret_key = key


# выводим секретный ключ в терминал
print("Секретный ключ:", key)


# осоновной обработчик запросов (головной центр или домашняя старница)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# обработчик старницы about
@app.route('/about')
def about():
    return render_template('about.html')

# обработчик старницы help
@app.route('/help')
def help():
    return render_template('help.html')

# обработчик старницы forum
@app.route('/forum')
def forum():
    return render_template('forum.html')

# личный кабинет пользователей
@app.route('/account')
def account():
    return render_template('account.html')


# GET-POST метод для авторизации пользователя и показа формы
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if checkLogin(username, password):
            session['username'] = username
            return redirect(url_for('account'))
        else:
            return 'Неверные учетные данные'

    return render_template('login.html')


# <------------------- ОБРАБОТЧИК ЛОГИКО ЗАВИСИМЫХ СТРУКТУР POST ЗАПРОСОВ ----------------------->


# GET-POST метод для авторизации пользователя и показа формы
@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ago_password = request.form['ago_password']
        
        if password == ago_password:
            if addNewUser(username, password):
                session['username'] = username
                return redirect(url_for('account'))
            else:
                return 'Неверные учетные данные'
        else:
            return "пароли не совпадают"

    return render_template('registration.html')


# POST метод выхода из аккаунта
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('/'))


@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    answer = "Ответ на вопрос"
    return render_template('forum.html', question=question, answer=answer)



# <---------------- ОБРАБОТЧИКИ ОШИБОК ------------------->
# Обработчик ошибки 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404), 404


# Обработчик ошибки 500
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500), 500


# Обработчик ошибки 505
@app.errorhandler(505)
def http_version_not_supported_error(error):
    return render_template('error.html', error_code=505), 505



# <------------------- ОБРАБОТЧИКИ КНОПОК ------------------->
# обработчик принятия post запроса от кнопки с каким-то параметром
@app.route('/handle_button_click', methods=['POST'])
def handle_button_click():
    # Этот код будет выполняться при нажатии на кнопку
    # Здесь вы можете добавить любую логику, которую хотите выполнить при нажатии на кнопку
    print("Кнопка была нажата!")
    return "Кнопка была нажата!"


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
