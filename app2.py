from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import hmac
import hashlib
from urllib.parse import unquote
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Для сессий

# токен бота
BOT_TOKEN = 'TELEGRAM_TOKEN'


def verify_telegram_data(data):
    """Проверка подлинности данных от Telegram"""
    # Извлекаем хеш из данных
    received_hash = data.get('hash')
    if not received_hash:
        return False

    # Удаляем хеш и создаем строку для проверки
    data_check = {k: v for k, v in data.items() if k != 'hash'}
    data_check_string = '\n'.join([f"{k}={data_check[k]}" for k in sorted(data_check.keys())])

    # Создаем секретный ключ
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()

    # Создаем хеш для сравнения
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Проверяем срок действия (данные старше 1 часа недействительны)
    auth_date = int(data.get('auth_date', 0))
    if datetime.now().timestamp() - auth_date > 3600:
        return False

    return calculated_hash == received_hash


@app.route('/')
def index():
    # Проверяем, авторизован ли пользователь (через сессию)
    is_authenticated = session.get('telegram_id') is not None
    return render_template('index.html', is_create_page=False, is_authenticated=is_authenticated)


@app.route('/create')
def create():
    return render_template('create.html', is_create_page=True)


@app.route('/auth', methods=['POST'])
def auth():
    """Обработка авторизации от Telegram"""
    data = request.form.to_dict()

    if verify_telegram_data(data):
        # Сохраняем ТОЛЬКО идентификатор в сессии (без БД!)
        session['telegram_id'] = data['id']
        session['first_name'] = data.get('first_name', '')
        session['username'] = data.get('username', '')
        session['photo_url'] = data.get('photo_url', '')
        session['auth_date'] = data['auth_date']

        # Перенаправляем на главную
        return redirect(url_for('index'))
    else:
        return "Ошибка авторизации", 403


@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    # Эта функция больше не нужна — вход только через Telegram
    return redirect(url_for('create'))


if __name__ == '__main__':
    app.run(debug=True)