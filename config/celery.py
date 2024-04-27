import os
from datetime import timedelta

from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    'check_habits_reminder': {
        'task': 'habits.tasks.check_habits_reminder',
        'schedule': timedelta(minutes=1),  # Проверка каждую минуту
    },
}
