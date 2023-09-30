import logging
from telegram.ext import *
import mysql.connector

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

import responses

mydb = mysql.connector.connect(host='localhost', user='root', password='password123', database='telegrambot')

cursor = mydb.cursor()


API_KEY = '6037321190:AAHGwdvHhJi78wQAz5ALTHmN5jEWZspAuGg'

# set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

#conversation states
WAITING_FOR_FIRST_NAME = 1
WAITING_FOR_LAST_NAME = 2
WAITING_FOR_PHONE_NUMBER = 3
WAITING_FOR_DEPARTMENT = 4
WAITING_FOR_POSITION = 5

# Dictionary to story user data
user_data = {}


def signup_command(update, context):
    update.message.reply_text("Please enter your first name:")
    context.user_data['state'] = WAITING_FOR_FIRST_NAME
    return WAITING_FOR_FIRST_NAME

def response_collector(update,context):


    user_id = update.message.from_user.id
    user_response = update.message.text

    # Store the user's response in the user_data dictionary based on the conversation state
    state = context.user_data['state']
    if state == WAITING_FOR_FIRST_NAME:
        user_data[user_id] = {'first_name': user_response}
        context.user_data['state'] = WAITING_FOR_LAST_NAME
        update.message.reply_text("Please enter your last name:")
    elif state == WAITING_FOR_LAST_NAME:
        user_data[user_id]['last_name'] = user_response
        context.user_data['state'] = WAITING_FOR_PHONE_NUMBER
        update.message.reply_text("Please provide your phone number:")
    elif state == WAITING_FOR_PHONE_NUMBER:
        user_data[user_id]['phone_number'] = user_response
        context.user_data['state'] = WAITING_FOR_DEPARTMENT
        update.message.reply_text("What department do you volunteer in?")
    elif state == WAITING_FOR_DEPARTMENT:
        user_data[user_id]['department'] = user_response
        context.user_data['state'] = WAITING_FOR_POSITION
        update.message.reply_text("Are you a lead in your department? (YES/NO)")
    elif state == WAITING_FOR_POSITION:
        user_data[user_id]['position'] = user_response
        update.message.reply_text("Successful!")

    first_name = user_data[user_id].get('first_name', 'Unknown')
    last_name = user_data[user_id].get('last_name', 'Unknown')
    phone_number = user_data[user_id].get('phone_number', 'Unknown')
    department = user_data[user_id].get('department', 'Unknown')
    position = user_data[user_id].get('position', 'Unknown')

    # sets user idea as a tuple
    sender_id = (update.message.from_user.id,)
    id = (user_id,)
    sql_command = "INSERT INTO user (id, firstName, lastName, phoneNumber, Department, Position) VALUES (%s, NULL, NULL,NULL, NULL, NULL);"
    cursor.execute(sql_command, id)
    mydb.commit()

    info = (first_name, last_name, phone_number, department, position)

    # sends data to database
    sql_command = "INSERT INTO user (id, firstName, lastName, phoneNumber, Department, Position) VALUES (NULL, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command,info)
    mydb.commit()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('signup', signup_command)],  # Start the conversation with the /start command
    states={
        WAITING_FOR_FIRST_NAME: [MessageHandler(Filters.text, response_collector)],
        WAITING_FOR_LAST_NAME: [MessageHandler(Filters.text, response_collector)],
        WAITING_FOR_PHONE_NUMBER: [MessageHandler(Filters.text, response_collector)],
        WAITING_FOR_DEPARTMENT: [MessageHandler(Filters.text, response_collector)],
        WAITING_FOR_POSITION: [MessageHandler(Filters.text, response_collector)],
    },
    fallbacks=[],
)


def budgetrequest_command(update, context):
        update.message.reply_text('Hi I am here to help')

def receiptsubmission_command(update, context):
            update.message.reply_text('This is a custom command')



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



    # Log all Errors
    dp.add_error_handler(error)

    # Run the Bot
    updater = Updater(token='6037321190:AAHGwdvHhJi78wQAz5ALTHmN5jEWZspAuGg', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()