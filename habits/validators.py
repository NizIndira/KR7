from rest_framework.serializers import ValidationError


class RelatedOrRewardHabitValidator:
    """Исключить одновременный выбор связанной
     привычки и указания вознаграждения"""
    def __call__(self, value):
        related_habit = value.get('related_habit')
        reward = value.get('reward')

        if related_habit and reward:
            raise ValidationError('Вы должны указать связанную привычку,'
                                  ' или вознаграждение.')


class ExecuteTimeHabitValidator:
    """Время выполнения должно быть не больше 120 секунд."""
    def __call__(self, value):
        execute_time = value.get('execute_time')
        if execute_time > 120:
            raise ValidationError('Время на выполнение не более 120 секунд.')


class RelatedIsPleasantHabitValidator:
    """В связанные привычки могут попадать только
     привычки с признаком приятной привычки"""
    def __call__(self, value):
        related_habit = value.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError('В связанные привычки могут попадать только'
                                  ' привычки с признаком приятной привычки')
        return value


class PleasantHabitValidator:
    """У приятной привычки не может быть
     вознаграждения или связанной привычки."""
    def __call__(self, value):
        is_pleasant = value.get('is_pleasant')
        related_habit = value.get('related_habit')
        reward = value.get('reward')
        if is_pleasant:
            if related_habit or reward:
                raise ValidationError(
                    'У приятной привычки не может быть'
                    ' вознаграждения или связанной привычки.')


class PeriodicityHabitValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    def __call__(self, value):
        periodicity = value.get('periodicity')
        if periodicity > 7:
            raise ValidationError('Нельзя выполнять привычку реже,'
                                  ' чем 1 раз в 7 дней')
