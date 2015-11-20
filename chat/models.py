#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re

from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    u"Цепочка сообщений"
    owner = models.ForeignKey(User)


class Message(models.Model):
    u"Сообщение"
    thread = models.ForeignKey(Thread)
    sender = models.ForeignKey(User, null=True, blank=True)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    @property
    def urls(self):
        u"Список адресов сайтов встречающихся в строке"
        return re.findall(u"https?://[-a-zA-Z0-9_./]+/*", self.text)

    @property
    def prev_sender_message(self):
        u"Прерыдущее сообщение от sender"
        prev_messages = self.thread.message_set.filter(
            sender__isnull=False
        ).exclude(
            id=self.id
        ).order_by("-datetime", "-id")

        return (list(prev_messages) or [None, ])[0]

    @property
    def is_command_get_site_title(self):
        return re.match(u"^Бот, дай мне заголовок сайта.*$", self.text, flags=re.IGNORECASE)

    @property
    def is_command_get_sites_title(self):
        return re.match(
            u"^Бот, дай мне все варианты заголовков с сайтов.*$",
            self.text,
            flags=re.IGNORECASE
        )

    @property
    def is_command_get_site_h1(self):
        return re.match(
            u"^Бот, дай мне H1 с сайта.*$",
            self.text,
            flags=re.IGNORECASE
        )

    @property
    def is_command_save_information(self):
        return re.match(
            u"^Бот, сохрани для меня информацию.*$",
            self.text,
            flags=re.IGNORECASE
        )

    @property
    def is_command_get_remember(self):
        return re.match(
            u"^Бот, напомни мне.*$",
            self.text,
            flags=re.IGNORECASE
        )

    @property
    def is_command_get_last_information(self):
        return re.match(
            u"^Бот, верни мне последнюю сохранененную информацию.*$",
            self.text,
            flags=re.IGNORECASE
        )


class Information(models.Model):
    u"Информация"
    thread = models.ForeignKey(Thread)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
