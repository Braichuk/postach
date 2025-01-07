from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

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

# Оновлення статусу заявки
async def update_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    if chat_id in applications:
        applications[chat_id]["status"] = "Виконано"
        await query.edit_message_text(text="Статус заявки оновлено: Виконано")
    else:
        await query.edit_message_text(text="Заявка не знайдена.")

# Перегляд статусу заявки
async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in applications:
        status = applications[chat_id].get("status", "Не знайдено")
        await update.message.reply_text(f"Статус вашої заявки: {status}")
    else:
        await update.message.reply_text("Заявка не знайдена.")

# Основна програма
def main():
    # Ваш токен від BotFather
    TOKEN = '7885890312:AAEd1pmNImB2Ec0u4P8yZiyrN3Y4myop4t4'

    # Ініціалізація бота через Application
    application = Application.builder().token(TOKEN).build()

    # Додати обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("new_request", new_request))
    application.add_handler(CommandHandler("check_status", check_status))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
      app.run(port=int(os.environ.get('PORT', 5000)))
