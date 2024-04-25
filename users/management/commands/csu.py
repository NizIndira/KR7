import os

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Класс для создания суперюзера"""
    def handle(self, *args, **options):
        superuser_email = os.getenv('SUPERUSER_EMAIL')
        if User.objects.get(email=superuser_email):
            self.stdout.write(self.style.ERROR(f'Superuser with email "{superuser_email}" already exists.'))
            return

        user = User.objects.create(
            email=os.getenv('SUPERUSER_EMAIL'),
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Superuser with email "{superuser_email}" successfully created.'))
