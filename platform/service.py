from flask import Flask, render_template
import json


PORT: int = 8080
HOST: str = "localhost"


app = Flask(__name__)

# соновной обработчик запросов (головной центр или домашняя старница)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# обработчик ошибки 404 пользователя (не найден файл или каталог)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# обработчик принятия post запроса от кнопки с каким-то параметром
@app.route('/handle_button_click', methods=['POST'])
def handle_button_click():
    # Этот код будет выполняться при нажатии на кнопку
    # Здесь вы можете добавить любую логику, которую хотите выполнить при нажатии на кнопку
    print("Кнопка была нажата!")
    return "Кнопка была нажата!"


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
