from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import os

# Ініціалізація Flask
app = Flask(__name__)

# Словник для заявок
applications = {}

# Функція для команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привіт! Я ваш бот для заявок. Використовуйте команду /new_request для створення заявки.")

# Функція для створення нової заявки
async def new_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    applications[chat_id] = {"status": "На розгляді"}
    await update.message.reply_text("Заявка створена! Введіть назву матеріалу.")

# Перегляд статусу заявки
async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in applications:
        status = applications[chat_id].get("status", "Не знайдено")
        await update.message.reply_text(f"Статус вашої заявки: {status}")
    else:
        await update.message.reply_text("Заявка не знайдена.")

# Ініціалізація Telegram Application
TOKEN = os.environ.get("7885890312:AAEd1pmNImB2Ec0u4P8yZiyrN3Y4myop4t4")  # Токен через змінну середовища
telegram_app = Application.builder().token(TOKEN).build()

# Додати обробники команд
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("new_request", new_request))
telegram_app.add_handler(CommandHandler("check_status", check_status))

# Вебхук для обробки запитів
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return 'OK'

if __name__ == '__main__':
    # Встановлюємо webhook
    webhook_url = f'https://api.render.com/deploy/srv-ctug22bqf0us73f3qjs0?key=JnaPjvDIAkw'
    telegram_app.bot.set_webhook(url=webhook_url)

    # Запуск Flask сервера
    app.run(port=int(os.environ.get('PORT', 5000)))
