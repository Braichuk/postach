from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import os

# Ініціалізація Flask для webhook
app = Flask(__name__)

# Словник для заявок
applications = {}

# Функція для команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привіт! Я ваш бот для заявок. Використовуйте команду /new_request для створення заявки."
    )

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

# Встановлення webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, application.bot)
    application.update_queue.put_nowait(update)
    return 'OK'

# Основна програма
def main():
    # Отримання токена з середовища
    TOKEN = os.environ.get("7885890312:AAGwArM_oD2HjGYzGv326WnrnkyAP8NXUb4")
    if not TOKEN:
        raise ValueError("Токен Telegram не знайдено!")

    # Ініціалізація бота через Application
    global application
    application = Application.builder().token(TOKEN).build()

    # Додати обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("new_request", new_request))
    application.add_handler(CommandHandler("check_status", check_status))

    # Встановлюємо webhook для Telegram
    application.bot.set_webhook(url='https://api.render.com/deploy/srv-ctug22bqf0us73f3qjs0?key=JnaPjvDIAkw')

    # Запуск Flask сервера
    app.run(port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
