from django.conf.urls import patterns, url

urlpatterns = patterns('chat.views',
    url(r'^$', 'chat_view'),
    url(r'^save_name/$', 'save_name'),
    url(r'^send_message/$', 'send_message_view'),
    url(r'^messages_view/$', 'messages_view'),
)
