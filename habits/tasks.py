import os
import requests
from celery import shared_task
from habits.models import Habit
from datetime import datetime, timezone


@shared_task
def send_habit_reminder():
    api_telegram_token = os.getenv('TELEGRAM_API_TOKEN')
    url = f'https://api.telegram.org/bot{api_telegram_token}/sendMessage'
    habits = Habit.objects.all()
    for habit in habits:
        now = datetime.now()
        now = datetime.now(tz=timezone.utc)
        if habit.last_notification is None or habit.last_notification.date() < now.date():
            message = f"Напоминание:\n необходимо выполнить привычку '{habit.action}' за: {habit.execute_time} секунд."
            requests.post(url, data={
                'chat_id': habit.user.telegram_chat_id,
                'text': message
                })

        habit.last_notification = datetime.now(tz=timezone.utc)
        habit.save()
