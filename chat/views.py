#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from lazysignup.decorators import allow_lazy_user

from chat.models import Thread

from chat.utils import json_response, send_message


@allow_lazy_user
def send_message_view(request):
    if not request.method == "POST":
        return HttpResponse("Пожалуйста, используйте метод.")

    if not request.user.last_name:
        return render_to_response(
            'name.html',
            {},
            context_instance=RequestContext(request)
        )

    message_text = request.POST.get("message")

    if not message_text:
        return HttpResponse("Нет сообщения.")

    if len(message_text) > 10000:
        return HttpResponse("Сообщение слишком длинное.")

    thread_id = request.POST.get("thread_id")

    send_message(thread_id, request.user.id, message_text)

    return json_response({"status": "ok"})


@allow_lazy_user
def save_name(request):
    user = request.user
    user.last_name = request.POST.get("user_name")
    user.save()

    return json_response({"status": "ok"})


@allow_lazy_user
def chat_view(request):
    user = request.user
    if not user.last_name:
        return render_to_response(
            'name.html',
            {},
            context_instance=RequestContext(request)
        )

    thread = Thread.objects.get_or_create(owner=user)[0]

    now = datetime.now()
    messages = thread.message_set.filter(
        datetime__lte=now
    ).order_by("-datetime", "-id")[:20]

    return render_to_response(
        'chat.html',
        {
            "thread_id": thread.id,
            "user": user,
            "messages": messages,
        },
        context_instance=RequestContext(request)
    )


@allow_lazy_user
def messages_view(request):
    user = request.user
    if not user.last_name:
        return render_to_response(
            'name.html',
            {},
            context_instance=RequestContext(request)
        )

    thread = Thread.objects.get_or_create(owner=user)[0]

    now = datetime.now()
    messages = thread.message_set.filter(
        datetime__lte=now
    ).order_by("-datetime", "-id")

    limit = request.GET.get("limit")
    if limit:
        messages = messages[:limit]

    return render_to_response(
        'messages.html',
        {
            "thread_id": thread.id,
            "user": user,
            "messages": messages,
        },
        context_instance=RequestContext(request)
    )
