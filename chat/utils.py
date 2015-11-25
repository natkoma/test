#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from datetime import timedelta
import json
import re
import requests
from lxml import html

from django.http import HttpResponse

from chat.models import Message, Information


def json_response(obj):
    """
    This function takes a Python object (a dictionary or a list)
    as an argument and returns an HttpResponse object containing
    the data from the object exported into the JSON format.
    """
    return HttpResponse(json.dumps(obj), content_type="application/json")


def get_elemet_text(url, element_name):
    u"""
    Возвращает тестовое содержание первого встреченного элемента на указанной странице.
    """
    response = requests.get(url)
    # Преобразование тела документа в дерево элементов (DOM)
    parsed_body = html.fromstring(response.text)
    # Выполнение xpath в дереве элементов
    for i in range(20):
        elemet_text = parsed_body.xpath('/' * i + element_name + '/text()')
        if elemet_text:
            return elemet_text[0]


def get_site_title(message):
    u"""
    Получает заголовок сайта.
    """
    text = u"В запросе нет или некорректно задан адрес сайта"
    url = message.urls[0] if message.urls else None
    if url:
        try:
            text = get_elemet_text(url, 'title')
        except:
            text = u"Не удалось получить заголовок сайта"
    return text


def get_sites_title(message):
    u"""
    Получает заголовки сайтов.
    """
    text = u"В запросе нет или некорректно заданы адреса сайтов"
    titles = []
    for url in message.urls:
        try:
            titles.append(u"Заголовки %s с сайта %s" % (get_elemet_text(url, 'title'), url))
        except:
            titles.append(u"Не удалось получить заголовок с сайта %s" % url)
    if titles:
        text = u". ".join(titles)
    return text


def get_site_h1(message):
    u"""
    Получает H1 сайта.
    """
    text = u"В запросе нет или некорректно задан адрес сайта"
    url = message.urls[0] if message.urls else None
    if url:
        try:
            text = get_elemet_text(url, 'h1')
        except:
            text = u"Не удалось получить H1 сайта"
    return text


def save_information(message):
    u"""
    Запомнить информацию.
    """
    text = None
    info = re.findall(
        u"Бот, сохрани для меня информацию *(.*)",
        message.text,
        flags=re.IGNORECASE
    )
    if info and info[0]:
        text = info[0]
    else:
        prev_sender_message = message.prev_sender_message
        information = (
            get_site_title(prev_sender_message) or
            get_site_h1(prev_sender_message) or
            get_sites_title(prev_sender_message)
        )
        if information:
            text = u"Время: %s; сайт: %s; информация: %s" % (
                prev_sender_message.datetime.strftime("%d:%m:%Y %H:%M:%S"),
                prev_sender_message.urls[0],
                information
            )
    if text:
        Information(thread=message.thread, text=text).save()
        text = u"Была сохранена информация: %s" % text
    return text


def get_remember(message):
    u"""
    Получить напоминание.
    """
    text = None
    parameters = re.findall(
        u"Бот, напомни мне (.*) через (\d+\.?,?\d*) (секунд|минут).*$",
        message.text,
        flags=re.IGNORECASE
    )
    if parameters and parameters[0]:
        info, time, time_unit = parameters[0]
        time = re.sub(u",", u".", time, flags=re.IGNORECASE)
        time = float(time)
        if time_unit == u"минут":
            time = time * 60
        remember = Message(
            thread=message.thread,
            text=u"Напоминаю: %s" % info,
            datetime=message.datetime
        )
        remember.save()
        remember.datetime += timedelta(seconds=time)
        remember.save()

        text = u"Задачу понял и поставил себе в очередь"
    return text


def get_last_information(message):
    u"""
    Получить последнюю сохраненную информацию.
    """
    informations = message.thread.information_set.all().order_by("-datetime", "-id")
    return informations[0].text if informations else u"Нет сохраненной информации"


def create_answer(message):
    u"""
    Создание ответа бота.
    """
    # Удаляем пробелы в начале и конце строки и символы переноса строки.
    message.text = re.sub("^\s+|\n|\r|\s+$", "", message.text)
    # Несколько пробелов подряд заменяем на один.
    message.text = re.sub(" +", " ", message.text)

    if re.match(u'^Бот.*$', message.text) is not None:
        text = None

        if message.is_command_get_site_title:
            text = get_site_title(message)
        elif message.is_command_get_sites_title:
            text = get_sites_title(message)
        elif message.is_command_get_site_h1:
            text = get_site_h1(message)
        elif message.is_command_save_information:
            text = save_information(message)
        elif message.is_command_get_remember:
            text = get_remember(message)
        elif message.is_command_get_last_information:
            text = get_last_information(message)

        if text is None:
            text = u"Не корректно указана команда"

        Message(thread=message.thread, text=text).save()


def send_message(thread_id, sender_id, message_text):
    u"""
    Отправка сообщения и создание ответв.
    """

    # Сохранение сообщения
    message = Message(
        thread_id=thread_id,
        text=message_text,
        sender_id=sender_id
    )
    message.save()

    # Создание ответа
    create_answer(message)
