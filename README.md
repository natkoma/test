1) Установить необходимые зависимости описанные в файле requirements.txt

2) В файле settings.py прописать соединение с базой данных PostgreSQL или другой

3) Применить миграции:
python  manage.py migrate

4) Запустить сервер:
python  manage.py runserver

5) Перейти по адресу:
http://127.0.0.1:8000/
