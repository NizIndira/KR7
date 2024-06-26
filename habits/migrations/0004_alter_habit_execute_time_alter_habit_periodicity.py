# Generated by Django 4.2.11 on 2024-04-26 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_alter_habit_execute_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='execute_time',
            field=models.IntegerField(blank=True, default=120, null=True, verbose_name='время на выполнение'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.IntegerField(blank=True, null=True, verbose_name='периодичность'),
        ),
    ]
