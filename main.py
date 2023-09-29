import logging
from telegram.ext import *
import mysql.connector
import responses

mydb = mysql.connector.connect(host="locaclhost", user="root", host="password123")
API_KEY = '6037321190:AAHGwdvHhJi78wQAz5ALTHmN5jEWZspAuGg'

# set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

def signup_command(update, context):
    update.message.reply_text('Enter your first name')
    update.message.reply_text('Enter your last name')
    update.message.reply_text('Enter your phone number')
    update.message.reply_text('Enter the department you do seva in')
    update.message.reply_text('Are you the lead of this department? (YES/NO)')


def budgetrequest_command(update, context):
        update.message.reply_text('Hi I am here to help')

def receiptsubmission_command(update, context):
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
    dp.add_handler(CommandHandler('signup', signup_command))
    dp.add_handler(CommandHandler('budgetrequest',  budgetrequest_command))
    dp.add_handler(CommandHandler('receiptsubmission', receiptsubmission_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all Errors
    dp.add_error_handler(error)

    # Run the Bot
    updater.start_polling(2.0)
    updater.idle()