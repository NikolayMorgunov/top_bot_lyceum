from telegram.ext import CommandHandler, MessageHandler, Filters

from . import auth
from . import get_top
from . import homeworks
from . import mojno
from . import start

METHODS = [
    CommandHandler('start', start.on_start),
    MessageHandler(Filters.text & Filters.group, mojno.send_msg),
    CommandHandler('top', get_top.send_msg),
    CommandHandler('top-activate', get_top.top_activate),
    auth.conv_handler,
    homeworks.conv_handler
]
