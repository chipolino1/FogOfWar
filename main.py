from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# Стартова команда для надсилання кнопки вибору локації
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Створюємо кнопку для вибору локації через Google Maps
    keyboard = [
        [InlineKeyboardButton("Оберіть локацію на мапі", url="https://www.google.com/maps")]
    ]
    
    # Відправляємо повідомлення з кнопкою
    await update.message.reply_text(
        "Привіт! Виберіть локацію на мапі: 🌍", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Обробка локації після того, як користувач надіслав її
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отримуємо координати локації
    location = update.message.location
    latitude = location.latitude
    longitude = location.longitude
    
    # Надсилаємо координати назад користувачу
    await update.message.reply_text(
        f"Твоя локація: \nШирота: {latitude}\nДовгота: {longitude}"
    )

# Основний функціонал для запуску бота
def main():
    from telegram.ext import Application

    application = Application.builder().token("YOUR_BOT_API_TOKEN").build()

    # Додаємо обробники команд та локації
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))  # Обробка локації

    application.run_polling()

if __name__ == '__main__':
    main()
