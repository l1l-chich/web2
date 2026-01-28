from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', is_create_page=False)

@app.route('/create')
def create():
    return render_template('create.html', is_create_page=True)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Здесь добавьте сохранение в базу данных
    print(f"Регистрация: {username}, {email}")
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Здесь добавьте проверку логина и пароля
    print(f"Вход: {username}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)