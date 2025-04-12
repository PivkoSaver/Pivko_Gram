from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Перенаправление с главной страницы на логин
@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (nickname TEXT, password TEXT)')
        c.execute('INSERT INTO users (nickname, password) VALUES (?, ?)', (nickname, password))
        conn.commit()
        conn.close()

        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE nickname = ? AND password = ?', (nickname, password))
        user = c.fetchone()
        conn.close()

        if user:
            return redirect('/chat')
        else:
            return 'Неверный логин или пароль'
    return render_template('login.html')

@app.route('/chat')
def chat():
    return 'Добро пожаловать в чат! (пока просто текст)'

if __name__ == '__main__':
    app.run(debug=True)
