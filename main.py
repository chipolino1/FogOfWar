from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
import os
import math
import psycopg2

# Отримання з'єднувальних даних з Railway
host = "postgres.railway.internal"
dbname = "railway"
user = "postgres"
password = "zNBVWTNZedTfaFNTpCdAIgdQONutixEg"


# Підключення до бази даних
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
cursor = conn.cursor()

# Виконання SQL запитів
cursor.execute("SELECT * FROM Kvadrat")

result = cursor.fetchall()
print(result)


# Закриття з'єднання
cursor.close()
conn.close()




# Координати центру (м. Вінниця)
latitude_center = 49.2328
longitude_center = 28.4682

# Радіус (10 км)
radius = 10000  # в метрах

# Розмір квадрата (2*2 метри)
square_size = 2

# Функція для обчислення відстані між двома точками за допомогою формули Хаверсина
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Радіус Землі в метрах
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # відстань в метрах

# Перевести координати в метри
def gps_to_meters(lat, lon):
    distance_lat = haversine(latitude_center, longitude_center, lat, longitude_center)
    distance_lon = haversine(latitude_center, longitude_center, latitude_center, lon)
    return distance_lat, distance_lon

# Обчислити номер квадрата за GPS координатами
def get_square_number(lat, lon):
    # Перевести координати в метри
    dist_lat, dist_lon = gps_to_meters(lat, lon)
    
    # Визначити координати квадрата
    square_x = int(dist_lon // square_size)
    square_y = int(dist_lat // square_size)
    
    # Нумерація квадратів починається з 1
    square_number = (square_y * 1000 + square_x) + 1  # Додаємо 1 для початку з 1
    return square_number


# Приклад використання:
latitude_input = 49.2400  # GPS координати
longitude_input = 28.4710

square_number = get_square_number(latitude_input, longitude_input)
print(f"Номер квадрата: {square_number}")



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