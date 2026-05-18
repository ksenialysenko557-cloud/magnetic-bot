from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import requests

TOKEN = "8696180753:AAFobb-WgJIC5YIu8YCFlwHwYwS_4lboVOE"

# Кнопки
keyboard = [
    ["📊 Прогноз", "💡 Советы"],
    ["☀️ О бурях", "📈 Уровень"],
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "━━━━━━━━━━━━━━\n"
        "☀️ MAGNETIC STORM BOT\n"
        "━━━━━━━━━━━━━━\n\n"
        "Добро пожаловать!\n"
        "Выберите нужный раздел 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# ПРОГНОЗ
async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

    response = requests.get(url)
    data = response.json()

    kp = float(data[-1]["kp_index"])

    if kp < 4:
        level = "🟢 Спокойно"
        advice = "Самочувствие у большинства людей нормальное."
    elif kp < 5:
        level = "🟡 Повышенная активность"
        advice = "Возможна лёгкая усталость."
    elif kp < 7:
        level = "🔴 Магнитная буря"
        advice = "Рекомендуется больше отдыха и воды."
    else:
        level = "🚨 Сильная буря"
        advice = "Лучше избегать нагрузок и стрессов."

    text = (
        "━━━━━━━━━━━━━━\n"
        "☀️ ПРОГНОЗ МАГНИТНЫХ БУРЬ\n"
        "━━━━━━━━━━━━━━\n\n"
        f"📊 Kp индекс: {kp}\n\n"
        f"{level}\n\n"
        f"💡 {advice}\n\n"
        "📅 Завтра ожидается\n"
        "умеренная солнечная активность."
    )

    await update.message.reply_text(text)

# СОВЕТЫ
async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "━━━━━━━━━━━━━━\n"
        "💡 РЕКОМЕНДАЦИИ\n"
        "━━━━━━━━━━━━━━\n\n"
        "💧 Пейте больше воды\n"
        "😴 Больше отдыхайте\n"
        "🚶 Чаще гуляйте\n"
        "📵 Избегайте стресса\n"
        "❤️ Следите за давлением"
    )

    await update.message.reply_text(text)

# ИНФОРМАЦИЯ
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "━━━━━━━━━━━━━━\n"
        "☀️ О МАГНИТНЫХ БУРЯХ\n"
        "━━━━━━━━━━━━━━\n\n"
        "Магнитные бури возникают\n"
        "из-за солнечной активности.\n\n"
        "Они могут влиять на:\n"
        "• давление\n"
        "• сон\n"
        "• самочувствие\n"
        "• настроение"
    )

    await update.message.reply_text(text)

# УРОВНИ
async def levels(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "━━━━━━━━━━━━━━\n"
        "📈 УРОВНИ АКТИВНОСТИ\n"
        "━━━━━━━━━━━━━━\n\n"
        "🟢 Kp 1–3 → спокойно\n"
        "🟡 Kp 4 → активность\n"
        "🔴 Kp 5–6 → буря\n"
        "🚨 Kp 7+ → сильная буря"
    )

    await update.message.reply_text(text)

# ОБРАБОТКА КНОПОК
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📊 Прогноз":
        await forecast(update, context)

    elif text == "💡 Советы":
        await advice(update, context)

    elif text == "☀️ О бурях":
        await info(update, context)

    elif text == "📈 Уровень":
        await levels(update, context)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
)

print("Бот запущен...")

app.run_polling()