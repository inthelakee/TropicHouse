import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import pandas as pd
from utils.image_handler import process_csv_and_images
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли мне CSV-файл с названиями растений — я всё обработаю.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file.file_name.endswith(".csv"):
        await update.message.reply_text("Пожалуйста, отправь CSV-файл.")
        return

    file_path = f"/tmp/{file.file_name}"
    new_file = await file.get_file()
    await new_file.download_to_drive(file_path)

    await update.message.reply_text("Обработка началась, это может занять несколько минут...")

    archive_path = process_csv_and_images(file_path)

    await update.message.reply_document(InputFile(archive_path))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()

if __name__ == "__main__":
    main()
