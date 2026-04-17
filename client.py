
---

## 🐍 **client.py (улучшенный, работает на ПК и Pydroid)**

```python
import urllib.request
import time
import ssl
import sys

SERVER_URL = "https://telegram-stars-prank.onrender.com/verify-codes.txt"

def check_code(user_code):
    try:
        context = ssl._create_unverified_context()
        req = urllib.request.Request(SERVER_URL)
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            data = response.read().decode('utf-8')
            return user_code in data
    except:
        return False

def loading_animation():
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    for i in range(12):
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r🔍 Проверка кода {frame}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r✅ Проверка завершена   ")

def main():
    print("\n" + "=" * 50)
    print("🎁 TELEGRAM STARS ACTIVATOR v2.0")
    print("=" * 50)
    print("\n⭐️ Получи 1000 звёзд бесплатно!\n")
    
    code = input("📱 Введите код с сайта: ").strip()
    
    if not code.isdigit() or len(code) != 4:
        print("\n❌ Неверный формат! Код должен состоять из 4 цифр.")
        input("\nНажми Enter для выхода...")
        return
    
    loading_animation()
    
    if check_code(code):
        print("\n✅ Код подтверждён!")
        time.sleep(0.5)
        
        print("\n🎉 ПОЗДРАВЛЯЕМ!")
        print("⭐️ На ваш аккаунт зачислено 1000 Telegram Stars! ⭐️")
        time.sleep(1.5)
        print("\n" + "😹" * 10)
        print("(шутка, конечно 😹)")
        print("Никаких звёзд не начислено. Это был пранк!")
        print("😹" * 10)
    else:
        print("\n❌ Неверный код!")
        print("Пожалуйста, обновите страницу и попробуйте ещё раз.")
        print("(код действителен только 5 минут)")
    
    print("\n" + "=" * 50)
    input("Нажми Enter для выхода...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Выход...")
