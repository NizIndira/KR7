from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCases(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Home',
            action='Drink juice',
            is_pleasant=True,
            execute_time=100
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            action='Drink water',
            related_habit=self.pleasant_habit,
            execute_time=100
        )

    def test_create_habit(self):
        '''Тестируем создание привычки'''
        data = {
            'action': 'Meditation',
            'place': 'Home',
            'related_action': self.pleasant_habit.pk,
            'execute_time': 100,
            'periodicity': 2
        }

        response = self.client.post(reverse('habits:habit_create'),
                                    data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_habit_list(self):
        '''Тестируем вывод списка привычек'''
        responce = self.client.get(
            reverse('habits:habit_list'),
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_200_OK
        )

    def test_one_habits_list(self):
        """Тестируем вывод одной привычки"""
        responce = self.client.get(
            reverse('habits:habit_retrieve', args=[self.habit.id]),
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_200_OK
        )

    def test_update_habits(self):
        '''Тестируем обновление привычки'''

        data = {
            'place': 'Office',
            'execute_time': 60,
            'periodicity': 3
        }
        response = self.client.patch(
            reverse('habits:habit_update', kwargs={'pk': self.habit.pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json()['place'],
            'Office'
        )

    def test_habit_delete(self):
        '''Тестируем удаление одной привычки'''

        response = self.client.delete(
            reverse('habits:habit_delete', args=[self.habit.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class HabitValidatorCreateTestCase(APITestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.client.force_authenticate(user=self.user)
        self.user.save()

        self.no_pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Home',
            action='Drink juice',
            is_pleasant=False,
            execute_time=100
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            action='Drink water',
            execute_time=100
        )

    def test_related_or_reward_HabitValidator(self):
        '''Тестируем валидатор: Исключить одновременный выбор
         связанной привычки и указания вознаграждения'''
        data = {
            "user": self.user.id,
            "action": "Test",
            "time": "2024-01-02T08:00:00",
            "place": "Test",
            "execute_time": 100,
            "periodicity": 4,
            "reward": "test",
            "related_habit": self.habit.id
        }

        responce = self.client.post(
            reverse('habits:habit_create'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_execute_time_HabitValidator(self):
        '''Тестируем валидатор: время выполнения
         должно быть не больше 120 секунд.'''
        data = {
            "user": self.user.id,
            "action": "Test",
            "time": "2024-01-02T08:00:00",
            "place": "Test",
            "is_pleasant": "True",
            "execute_time": 121,
            "periodicity": 4
        }
        responce = self.client.post(
            reverse('habits:habit_create'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_related_is_pleasant_HabitValidator(self):
        '''Тестируем валидатор: В связанные привычки могут
         попадать только привычки с признаком приятной привычки'''
        data = {
            "user": self.user.id,
            "action": "Test",
            "time": "2024-01-02T08:00:00",
            "place": "Test",
            "execute_time": 100,
            "periodicity": 4,
            "reward": "test",
            "related_habit": self.no_pleasant_habit.id
        }
        responce = self.client.post(
            reverse('habits:habit_create'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_pleasant_HabitValidator(self):
        '''Тестируем валидатор: У приятной привычки не может
         быть вознаграждения или связанной привычки'''
        data = {
            "user": self.user.id,
            "action": "Test",
            "time": "2024-01-01T08:00:00",
            "place": "Test",
            "execute_time": 100,
            "periodicity": 4,
            "reward": "test",
            "is_pleasant": "True"
        }
        responce = self.client.post(
            reverse('habits:habit_create'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_periodicity_HabitValidator(self):
        '''Тестируем валидатор: Нельзя выполнять
         привычку реже, чем 1 раз в 7 дней'''
        data = {
            "user": self.user.id,
            "action": "Test",
            "time": "2024-01-01T08:00:00",
            "place": "Test",
            "execute_time": 100,
            "periodicity": 10,
            "reward": "test"
        }
        responce = self.client.post(
            reverse('habits:habit_create'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )
