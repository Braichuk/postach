git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/repo-name.git
git push -u origin main
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Словник для заявок
applications = {}

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привіт! Я ваш бот для заявок. Використовуйте команду /new_request для створення заявки.")

# Команда для створення нової заявки
def new_request(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    applications[chat_id] = {"status": "На розгляді"}
    update.message.reply_text("Заявка створена! Введіть назву матеріалу.")

# Оновлення статусу заявки
def update_status(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    if chat_id in applications:
        applications[chat_id]["status"] = "Виконано"
        query.edit_message_text(text="Статус заявки оновлено: Виконано")
    else:
        query.edit_message_text(text="Заявка не знайдена.")

# Перегляд статусу заявки
def check_status(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id in applications:
        status = applications[chat_id].get("status", "Не знайдено")
        update.message.reply_text(f"Статус вашої заявки: {status}")
    else:
        update.message.reply_text("Заявка не знайдена.")

# Основна функція
def main():
    TOKEN = '7885890312:AAEd1pmNImB2Ec0u4P8yZiyrN3Y4myop4t4'
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Команди
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("new_request", new_request))
    dispatcher.add_handler(CommandHandler("check_status", check_status))
    dispatcher.add_handler(CallbackQueryHandler(update_status))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
