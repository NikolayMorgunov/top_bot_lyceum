from peewee import CharField, IntegerField, ForeignKeyField

from database import LyceumUser, BotModel


class ActiveTop(BotModel):
    chat_id = IntegerField(verbose_name='Telegram chat id', primary_key=True)
    tutor = ForeignKeyField(LyceumUser)
    token = CharField()
    url = CharField()
