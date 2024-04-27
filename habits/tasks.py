import logging
import requests
from datetime import datetime
from celery import shared_task
from django.conf import settings

from habits.models import Habit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_chat_id(telegram_username):
    api_telegram = f'https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/getUpdates'
    response = requests.get(api_telegram)
    data = response.json()

    if data.get('ok', False):
        for result in data.get('result', []):
            message = result.get('message', {})
            if 'from' in message and 'username' in message['from']:
                if telegram_username[1:] == message['from']['username']:
                    return message['from']['id']
    return None


@shared_task
def check_habits_reminder():
    current_day = datetime.now().weekday()
    datetime_now = datetime.now()

    habits = Habit.objects.filter(time=datetime_now)
    for habit in habits:
        logger.info(f"Processing habit: {habit.action}")
        if habit.user and habit.user.telegram_chat_id:
            if habit.periodicity == '0' or int(habit.periodicity) == current_day:
                message = f"Время выполнить: {habit.action}"
                send_reminder_to_user.delay(habit.user.telegram_chat_id, message)


@shared_task
def send_reminder_to_user(chat_id, message):
    api_telegram = f'https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(api_telegram, data=params)
    if response.status_code == 200:
        logger.info('Напоминание отправлено в Телеграм')
    else:
        logger.info(f'Ошибка при отправлении в Телеграм: {response.text}')
