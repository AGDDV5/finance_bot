import os
import logging
import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from dotenv import load_dotenv

from database import Session, User, Transaction
from texts import get_text
from utils import generate_dashboard, format_currency

load_dotenv()
TOKEN = os.getenv("8317433604:AAEYFaMyuUbySmhi3R5JYDxvlGaUhP1U3HI")

# States
SELECT_TYPE, SELECT_CATEGORY, CUSTOM_CATEGORY, ENTER_AMOUNT, REMINDER_DESC, REMINDER_DATE = range(6)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Database & Language Helpers (Same as before) ---
def get_user_lang(user_id):
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    lang = user.language if user else 'uz_lat'
    session.close()
    return lang

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = Session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()
    if not db_user:
        session.add(User(telegram_id=user.id))
        session.commit()
    session.close()
    
    keyboard = [['🇺🇿 O\'zbek (Lotin)', '🇺🇿 Ўзбек (Кирилл)']]
    await update.message.reply_text(
        "👋 Assalomu alaykum! Tilni tanlang / Тилни танланг:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    session = Session()
    user = session.query(User).filter_by(telegram_id=update.effective_user.id).first()
    if "Lotin" in text: user.language = 'uz_lat'
    elif "Кирилл" in text: user.language = 'uz_cyr'
    session.commit()
    lang = user.language
    session.close()
    await show_main_menu(update, lang)

async def show_main_menu(update: Update, lang):
    t = lambda k: get_text(lang, k)
    keyboard = [
        [t('expense'), t('income')],
        [t('report'), '⏰ Eslatmalar' if lang=='uz_lat' else '⏰ Эслатмалар']
    ]
    await update.message.reply_text(t('main_menu'), reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

# --- Reminder Logic ---
async def add_reminder_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nima uchun to'lov? (Masalan: Paynet)")
    return REMINDER_DESC

async def save_reminder_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['rem_desc'] = update.message.text
    await update.message.reply_text("Qachon eslatay? (Format: DD.MM.YYYY HH:MM)\nMisol: 25.01.2026 14:00")
    return REMINDER_DATE

async def save_reminder_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date_str = update.message.text
    try:
        rem_time = datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        # Add job to queue
        context.job_queue.run_once(send_reminder_job, rem_time, chat_id=update.effective_chat.id, data=context.user_data['rem_desc'])
        await update.message.reply_text(f"✅ Eslatma qo'yildi: {date_str}")
    except ValueError:
        await update.message.reply_text("⚠️ Sana formati noto'g'ri! Qayta kiriting (DD.MM.YYYY HH:MM)")
        return REMINDER_DATE
    
    return ConversationHandler.END

async def send_reminder_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"🔔 <b>Eslatma:</b> {job.data} to'lash vaqti keldi!", parse_mode='HTML')

# --- Main ---
def main():
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'O\'zbek|Ўзбек'), set_language))
    
    # Reminder Conversation
    rem_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r'⏰'), add_reminder_start)],
        states={
            REMINDER_DESC: [MessageHandler(filters.TEXT, save_reminder_desc)],
            REMINDER_DATE: [MessageHandler(filters.TEXT, save_reminder_date)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    application.add_handler(rem_handler)

    print("Bot ishladi...")
    application.run_polling()

if __name__ == '__main__':
    main()