web: gunicorn smrue.wsgi --log-file -
worker: celery -A smrue worker --app=smrue.tasks