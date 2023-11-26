web: gunicorn --bind :8000 --workers 2 --threads 2 soloconnect.wsgi:application
websocket: daphne -b 0.0.0.0 -p 5000 soloconnect.asgi:application