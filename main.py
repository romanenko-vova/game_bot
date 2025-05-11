import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

MAINMENU, KNB, TALK = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update — это словарь со всей информацией о том, что произошло
    # update.effective_user — вся инфа о человеке
    # update.effective_message — вся инфа о сообщении
    # update.effective_chat — вся инфа о диалоге
    #
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.effective_user.name}, привет!\n/knb",
    )
    return MAINMENU


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == "Привет":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Привет, как дела?"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.effective_message.text}",
        )


async def knb_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Ты попал в игру камень ножницы бумага",
    )
    return KNB


async def knb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ans = update.effective_message.text  # камень | ножницы | бумага
    comp_ans = "ножницы"
    if user_ans == "камень" and comp_ans == "ножницы":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Ты выиграл\nЯ выбрал ножницы\nЕсли хочешь выйти нажими /start",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    # Handler — обработчик
    # Обрабатывает какой-то вид update
    # entry_points — точки входа
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [CommandHandler("knb", knb_start)],
            KNB: [MessageHandler(filters.TEXT & ~filters.COMMAND, knb)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(conv_handler)

    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, talk))
    # & — и аnd
    # ~ — not не
    # | or или

    application.run_polling()
