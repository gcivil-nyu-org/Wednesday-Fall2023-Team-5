web: gunicorn --bind :8000 --workers 3 --threads 2 soloconnect.wsgi:application
websocket: daphne -b :: -p 5000 soloconnect.asgi:application