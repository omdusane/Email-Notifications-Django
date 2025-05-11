# celery command
celery -A core worker -P solo/threads/gevent -E -l info

# Flower Command
celery -A core.celery_app flower --basic_auth=admin:password

# Celery Beat Command
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler