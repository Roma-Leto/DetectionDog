import os
import DjangoProject.settings as settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.

# Установите модуль настроек Django по умолчанию для программы «celery».
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

broker_connection_retry_on_startup = True

app = Celery('DjangoProject')

app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    broker_connection_retry=True,  # Для предыдущих версий
    broker_connection_retry_on_startup=True,  # Для Celery 6.0 и выше
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# Использование здесь строки означает, что worker не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - namespace='CELERY' означает все ключи конфигурации, связанные с celery
# должны иметь префикс 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.

# Загрузить модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
