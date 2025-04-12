<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='threading')

online_users = set()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('index.html', nickname=user.nickname)

=======
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Перенаправление с главной страницы на логин
@app.route('/')
def index():
    return redirect('/login')

>>>>>>> 808b1f77a57fa89456a3922289714c741d01c032
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
<<<<<<< HEAD
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(nickname=nickname, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

=======

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (nickname TEXT, password TEXT)')
        c.execute('INSERT INTO users (nickname, password) VALUES (?, ?)', (nickname, password))
        conn.commit()
        conn.close()

        return redirect('/login')
    return render_template('register.html')

>>>>>>> 808b1f77a57fa89456a3922289714c741d01c032
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
<<<<<<< HEAD
        user = User.query.filter_by(nickname=nickname).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return render_template('login.html')

@socketio.on('connect')
def handle_connect():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        online_users.add(user.nickname)
        emit('user list', list(online_users), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        online_users.discard(user.nickname)
        emit('user list', list(online_users), broadcast=True)

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
=======

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
>>>>>>> 808b1f77a57fa89456a3922289714c741d01c032
