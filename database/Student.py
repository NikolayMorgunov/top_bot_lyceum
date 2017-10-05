from django.db.models import ForeignKey
from peewee import CharField, DateField, BooleanField

from database import LyceumGroup
from database.database import BotModel


class Student(BotModel):
    fullname = CharField()
    telegram_id = CharField()
    approved = BooleanField(default=False)
    lyceum_group = ForeignKey(LyceumGroup)


def update_or_create_user(telegram_id, **kwargs):
    student, is_created = Student.get_or_create(telegram_id=telegram_id)
    student.telegram_id = telegram_id  # TODO: check if set it manually necessary
    for key, val in kwargs.items():
        setattr(student, key, val)
    student.save()
    return student, is_created
