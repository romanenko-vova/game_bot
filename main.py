import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import os
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update — это словарь со всей информацией о том, что произошло
    # update.effective_user — вся инфа о человеке
    # update.effective_message — вся инфа о сообщении
    # update.effective_chat — вся инфа о диалоге
    # 
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.effective_user.name}, привет!")
    
async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == 'Привет':
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, как дела?")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.effective_message.text}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    # Handler — обработчик
    # Обрабатывает какой-то вид update
    # 
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, talk)
    application.add_handler(message_handler)
    
    
    application.run_polling()