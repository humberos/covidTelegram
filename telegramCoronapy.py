from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import subprocess
import time
import telegram
from datetime import datetime, timedelta
from time import sleep,time
import csv
import pandas as pd
from tabulate import tabulate



my_token = ""

def updateData():
    if os.stat('today.csv').st_mtime - time() < - 60: # check if last modified time is less bigger than 60 seconds   
        args = ['python3', 'worldometerCoronapy.py']
        subprocess.run(args)

def send(msg, chat_id, token=my_token):
    """
    Send a mensage to a telegram user specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)


def top10(bot, update):
    u_id = update.effective_user.id
    bot = telegram.Bot(token=my_token)
    updateData()
    bot.sendMessage(chat_id=u_id, text=("<pre>"+str(getLastCovid19Info(top=10))+"</pre>"), parse_mode='html')

def top20(bot, update):
    u_id = update.effective_user.id
    bot = telegram.Bot(token=my_token)
    updateData()
    bot.sendMessage(chat_id=u_id, text=("<pre>"+str(getLastCovid19Info(top=20))+"</pre>"),parse_mode='html')


def dump(obj):
    for attr in dir(obj):
        # if hasattr( obj, attr ):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))
        print("\r -------------------------------------- \r")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bot dedicated to show Coronavirus (COVID-19) updates.')


def listCommands(bot, update):
    update.message.reply_text('Nothing here...')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Nothing here...')


def echo(bot, update):
    """Echo the user message."""
    # update.message.reply_text(update.message.text)
    # u_id = update.effective_user.id
    update.message.reply_text("Beep Boop... Error")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def getLastCovid19Info(country='all',top=10):

    df = pd.read_csv('today.csv', nrows=top,index_col=False, usecols=[
                     "Country,Other", "TotalCases","TotalDeaths"])

    finalData = tabulate(
        df, headers=['Country', 'Cases', 'Deaths'], showindex="never")
    return str(finalData).replace('-','')


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(my_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("commands", listCommands))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("top10", top10))
    dp.add_handler(CommandHandler("top20", top20))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # loopCoronaBot()
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
