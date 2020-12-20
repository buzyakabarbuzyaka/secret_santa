from app.settings import TOKEN, DATA_DIR
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from app.load import give_secret_name

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Просто, блять, набери "хто?"')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('Ди на хуй! (если не понятьно чекай /help)')


def bind(update: Update, context: CallbackContext):
    telegram_id = update.effective_chat.username
    secret_answer = give_secret_name(telegram_id)

    if not secret_answer:
        update.message.reply_text('Ты не в банде, сорри(')
    else:
        is_already_given, secret_name = secret_answer
        if is_already_given:
            update.message.reply_text(f'Напоминаю, даришь подарок: {secret_name}')
        else:
            update.message.reply_text(f'Ты секретный санта для: {secret_name}')


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^хто\?$')), echo))
    dispatcher.add_handler(MessageHandler(Filters.regex('^хто\?$'), bind))

    updater.start_polling()
    updater.idle()


#TODO: Каждый может про себя что-то написать через бота (не пожелание)
#TODO: В отвте вместе с именем передавать telegram_id
#TODO: Комнаты для секретных подарков (разные списки)


if __name__ == '__main__':
    main()


