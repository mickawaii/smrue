web: gunicorn smrue.wsgi --log-file -
worker: celery -A smrue worker
beat: celery -A smrue beat