from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
import math
import os

TOKEN = os.getenv("BOT_TOKEN")
GRID_SIZE_METERS = 2

def get_grid_coords(lat, lon):
    lat_m = lat * 111320
    lon_m = lon * 40075000 * math.cos(math.radians(lat)) / 360
    grid_x = int(lat_m // GRID_SIZE_METERS)
    grid_y = int(lon_m // GRID_SIZE_METERS)
    return (grid_x, grid_y)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton("Надіслати локацію", request_location=True)]]
    await update.message.reply_text("Привіт! Надішли свою локацію 🌍", 
                                    reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True))

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loc = update.message.location
    grid = get_grid_coords(loc.latitude, loc.longitude)
    await update.message.reply_text(f"Ти в квадраті {grid} ✅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.LOCATION, location_handler))
app.run_polling()