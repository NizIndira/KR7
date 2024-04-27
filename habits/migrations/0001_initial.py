# Generated by Django 4.2.11 on 2024-04-25 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, max_length=255, null=True, verbose_name='место')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='время')),
                ('action', models.CharField(blank=True, max_length=255, null=True, verbose_name='действие')),
                ('is_pleasant', models.BooleanField(default=False, verbose_name='признак приятной привычки')),
                ('periodicity', models.CharField(choices=[(0, 'Daily'), (1, 'Every Monday'), (2, 'Every Tuesday'), (3, 'Every Wednesday'), (4, 'Every Thursday'), (5, 'Every Friday'), (6, 'Every Saturday'), (7, 'Every Sunday')], default='0', max_length=1, verbose_name='периодичность')),
                ('reward', models.CharField(blank=True, max_length=255, null=True, verbose_name='вознаграждение')),
                ('execute_time', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='время на выполнение')),
                ('is_public', models.BooleanField(default=False, verbose_name='признак публичности')),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit', verbose_name='связанная привычка')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'привычка',
                'verbose_name_plural': 'привычки',
            },
        ),
    ]
