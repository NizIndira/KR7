import os
import requests
from celery import shared_task
from habits.models import Habit
from users.models import User
from datetime import datetime


@shared_task
def send_habit_reminder():
    users = User.objects.all()

    for user in users:
        habits = Habit.objects.filter(user=user)

        for habit in habits:
            execute_time = habit.execute_time

            last_notification = habit.last_notification

            now = datetime.now()
            start_time = habit.time

            if (last_notification is None or last_notification.date() < now.date()) and start_time == now:
                send_notification.delay(habit, execute_time)


@shared_task
def send_notification(habit, execute_time):
    api_telegram_token = os.getenv('TELEGRAM_API_TOKEN')
    telegram_chat_id = habit.user.telegram_chat_id
    url = f'https://api.telegram.org/bot{api_telegram_token}/sendMessage'
    message = f"Напоминание:\n - необходимо выполнить привычку '{habit.action}' за: {execute_time} секунд."
    requests.post(url, data={
        'chat_id': telegram_chat_id,
        'text': message
    })

    habit.last_notification = datetime.now()
    habit.save()
