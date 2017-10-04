import locale
import methods
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import *

try:
    locale.setlocale(locale.LC_TIME, "ru_RU")
except:
    pass

updater = Updater(token=BOT_TOKEN)
j = updater.job_queue
dispatcher = updater.dispatcher

setup_logger(dispatcher)

dispatcher.add_handler(MessageHandler(Filters.text, methods.mojno.send_msg))

delta = datetime.time(hour=22, tzinfo=TIMEZONE)

# TODO: Write flexible datetime
j.run_daily(lambda a, b: methods.send_msg(a, b), time=datetime.time(12))

# Specify all methods below
dispatcher.add_handler(CommandHandler('top', methods.get_top.send_msg))

updater.start_polling()

updater.idle()
