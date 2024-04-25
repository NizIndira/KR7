from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Habit(models.Model):

    PERIODICITY_CHOICES = (
        (0, 'Daily'),
        (1, 'Every Monday'),
        (2, 'Every Tuesday'),
        (3, 'Every Wednesday'),
        (4, 'Every Thursday'),
        (5, 'Every Friday'),
        (6, 'Every Saturday'),
        (7, 'Every Sunday'),
    )

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
    periodicity = models.CharField(max_length=1, choices=PERIODICITY_CHOICES, default='0', verbose_name='периодичность')
    reward = models.CharField(max_length=255, verbose_name='вознаграждение', **NULLABLE)
    execute_time = models.PositiveSmallIntegerField(verbose_name='время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f'{self.owner} - {self.action}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
