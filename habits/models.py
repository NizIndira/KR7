from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Habit(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        **NULLABLE)
    place = models.CharField(max_length=255, verbose_name='место', **NULLABLE)
    time = models.TimeField(auto_now_add=True, verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие', **NULLABLE)
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    periodicity = models.IntegerField(verbose_name='периодичность', **NULLABLE)
    reward = models.CharField(max_length=255, verbose_name='вознаграждение', **NULLABLE)
    execute_time = models.IntegerField(default=120, verbose_name='время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    last_notification = models.DateTimeField(verbose_name='Дата и время последнего оповещения', **NULLABLE)

    def __str__(self):
        return f'{self.user} - {self.action}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
