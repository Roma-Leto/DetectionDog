# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# Это гарантирует, что приложение всегда будет импортировано при
# запуске Django, и Shared_task будет использовать это приложение.
import config

if config.IS_SERVER_NOTEBOOK:
    pass
else:
    from .celery import app as celery_app

    __all__ = ('celery_app', )
