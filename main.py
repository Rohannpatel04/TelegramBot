import logging
from telegram.ext import *
import responses

API_KEY = '6037321190:AAHGwdvHhJi78wQAz5ALTHmN5jEWZspAuGg'

# set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

def start_command(update, context):
    update.message.reply_text('Hi I am a Bot')

def help_command(update, context):
        update.message.reply_text('Hi I am here to help')

def custom_command(update, context):
            update.message.reply_text('This is a custom command')

def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    #bot response
    update.message.reply_text(text)

def error(update,context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all Errors
    dp.add_error_handler(error)

    # Run the Bot
    updater.start_polling(2.0)
    updater.idle()



