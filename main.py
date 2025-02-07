import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY  # Импортируем токен из config.py
import random

# Создаем объекты Bot и Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция получения погоды
def get_weather(city="Новосибирск"):
    lang = "ru"
    units = "metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&lang={lang}&units={units}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            return f"🌍 Город: {city}\n🌡 Температура: {temp}°C\n☁️ Погода: {weather_desc.capitalize()}"
        else:
            return "Не удалось получить прогноз погоды. Попробуйте позже."
    except Exception as e:
        return f"Ошибка: {e}"


# Обработчик команды /weather
@dp.message(Command("weather"))
async def weather(message: Message):
    weather_info = get_weather()
    await message.answer(weather_info)


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот. Используй /weather, чтобы узнать прогноз погоды для Новосибирска.")


# Обработчик команды /help
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Доступные команды:\n/start - Начать работу\n/weather - Прогноз погоды\n/help - Помощь" "\n/photo - Рандомная картинка")


# Обработчик команды /photo (рандомная картинка)
@dp.message(Command("photo"))
async def photo(message: Message):
    images = [
        "https://avatars.mds.yandex.net/i?id=9b513a670ee76376548f34a5c5660345589baf4d-9870356-images-thumbs&n=13",
        "https://avatars.mds.yandex.net/i?id=9c06b52cd440474f4866a3a5cc69d03bf0201fd6-7663084-images-thumbs&n=13",
        "https://avatars.mds.yandex.net/i?id=75c8f5559d1e51bddc7fac372513731b-5250945-images-thumbs&n=13"
    ]
    rand_photo = random.choice(images)
    await message.answer_photo(photo=rand_photo, caption="Это рандомная фотка")


# Обработчик входящих фото
@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ["Ого, какая фотка!", "Непонятно, что это такое", "Не отправляй мне такое больше"]
    await message.answer(random.choice(responses))


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())