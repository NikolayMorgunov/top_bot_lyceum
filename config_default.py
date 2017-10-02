import datetime

CUPS_OF = 6
BOT_TOKEN = ''
LOGIN = ''
PASSWORD = ''
LOGIN_URL = ''
DATA_URL = ''
SESSION_ID = ''
NUMBER_OF_KIDS = 5
COOLDOWN_FOR_LIST = datetime.timedelta(hours=3)

TITLES_LIST = [
    '👑 Бессменный лидер',
    '🥈 Неустанный преследователь',
    '🥉 Один из лучших',
    'Знает, что делает',
    'Хороший парень',
]

AFTERWORDS = [
    'Удачи ❤',
    'Этот список заговорён на удачу',
    'Похоже, кто-то хочет чай ☕',
    'Мои создатели выпили {} кружки чая ☕'.format(CUPS_OF),
]

NIGHTTIME_MESSAGES = [
    'Ночью доставка не работает. Добрых снов, добрый человек. 🚀',
    'Возвращайтесь на рассвете 🚀',
]

HEADERS = [
    'расклады следующие',
    'отметились',
    'зал славы',
]

COOLDOWN_MSGS = [
    'Терпение, друг',
    'Ещё рано',
    'Терпение, терпение',
]

CONTRIBUTORS = [
    102660981,  # mesenev
]
GREETING_TO_CONTRIBUTOR = [
    'Здравствуй, создатель',
]

GREETING_TO_SOMEONE = [
    'Приветствую, {name}',
]
