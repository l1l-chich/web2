from flask import Flask, render_template, request, redirect, url_for, session
import hmac
import hashlib
from urllib.parse import unquote
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Секретный ключ для сессий

# ТОКЕН БОТА!
BOT_TOKEN = 'TELEGRAM_TOKEN'


def verify_telegram_data(data):
    """
    Проверка подлинности данных от Telegram.
    Возвращает True, если данные подлинные, иначе False.
    """
    # Извлекаем хеш из данных
    received_hash = data.get('hash')
    if not received_hash:
        return False

    # Удаляем хеш и создаём строку для проверки
    data_check = {k: v for k, v in data.items() if k != 'hash'}
    data_check_string = '\n'.join([f"{k}={data_check[k]}" for k in sorted(data_check.keys())])

    # Создаём секретный ключ
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()

    # Создаём хеш для сравнения
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Проверяем срок действия (данные старше 1 часа недействительны)
    auth_date = int(data.get('auth_date', 0))
    if datetime.now().timestamp() - auth_date > 3600:
        return False

    # Сравниваем хеши
    return calculated_hash == received_hash


@app.route('/')
def index():
    is_authenticated = session.get('telegram_id') is not None
    return render_template('index.html',
                         is_create_page=False,
                         is_authenticated=is_authenticated,
                         current_page='index',
                         current_section='home')  # Можно менять в зависимости от якоря

@app.route('/about')
def about():
    """Страница 'О нас'"""
    return render_template('about.html', is_create_page=False)

@app.route('/catalog')
def catalog():
    return render_template('catalog.html', current_page='catalog')

@app.route('/blog')
def blog():
    return render_template('blog.html', current_page='blog')

@app.route('/create')
def create():
    """Страница входа через Telegram"""
    return render_template('create.html', is_create_page=True)


@app.route('/auth', methods=['POST'])
def auth():
    """
    Обработка авторизации от Telegram.
    Telegram отправляет сюда данные после успешного входа пользователя.
    """
    data = request.form.to_dict()

    print("Получены данные от Telegram:", data)  # Для отладки

    if verify_telegram_data(data):
        print("✅ Данные подтверждены!")

        # Сохраняем данные в сессии (без базы данных!)
        session['telegram_id'] = data['id']
        session['first_name'] = data.get('first_name', '')
        session['last_name'] = data.get('last_name', '')
        session['username'] = data.get('username', '')
        session['photo_url'] = data.get('photo_url', '')
        session['auth_date'] = data['auth_date']
        session['is_authenticated'] = True

        # Перенаправляем на главную
        return redirect(url_for('index'))
    else:
        print("❌ Ошибка авторизации!")
        return "Ошибка авторизации", 403


@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)