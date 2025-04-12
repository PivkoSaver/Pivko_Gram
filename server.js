const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
const http = require('http');

const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server);

// --- Настройка bodyParser для работы с POST-данными ---
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// --- Настройка сессии ---
app.use(session({
  secret: 'your_secret_key', // выбери свою секретную строку
  resave: false,
  saveUninitialized: false,
}));

// --- Простейшая in-memory база пользователей ---
// Структура: { username1: { password: '...', ...}, username2: {...} }
let users = {};

// --- Маршрут для статических файлов (чата) ---
app.use(express.static(__dirname));

// --- Маршрут для главной страницы ---
// Здесь мы проверяем, залогинен ли пользователь.
// Если нет, перенаправляем на страницу входа.
app.get('/', (req, res) => {
  if (req.session.user) {
    res.sendFile(path.join(__dirname, 'index.html'));
  } else {
    res.redirect('/login');
  }
});

// --- Страницы регистрации и входа ---
// Отдаём простые HTML-формы
app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, 'register.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

// --- Обработка POST-запросов для регистрации ---
app.post('/register', (req, res) => {
  const { username, password } = req.body;
  
  // Простейшие проверки
  if (!username || !password) {
    return res.send('Введите имя пользователя и пароль');
  }
  
  if (users[username]) {
    return res.send('Пользователь с таким именем уже существует. Попробуйте другое имя.');
  }
  
  // Создаём пользователя (в реальном проекте пароль нужно хэшировать)
  users[username] = { password };
  
  // Сохраняем данные в сессии
  req.session.user = { username };
  
  res.redirect('/');
});

// --- Обработка POST-запросов для входа ---
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  if (!username || !password) {
    return res.send('Введите имя пользователя и пароль');
  }
  
  const user = users[username];
  if (!user || user.password !== password) {
    return res.send('Неверное имя пользователя или пароль');
  }
  
  // Сохраняем данные в сессии
  req.session.user = { username };
  
  res.redirect('/');
});

// --- Маршрут для выхода ---
app.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    res.redirect('/login');
  });
});

// --- Socket.io обработка (доступна только для аутентифицированных пользователей) ---
io.use((socket, next) => {
  // Доступ к cookie сессии можно настроить через дополнительное middleware,
  // но для простоты предполагаем, что подключился только аутентифицированный пользователь.
  next();
});

io.on('connection', (socket) => {
  console.log('a user connected');
  
  socket.on('chat message', (msg) => {
    io.emit('chat message', msg);
  });
  
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
