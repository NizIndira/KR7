from rest_framework import serializers

from habits.models import Habit
from habits.validators import (RelatedOrRewardHabitValidator,
                               ExecuteTimeHabitValidator, RelatedIsPleasantHabitValidator,
                               PleasantHabitValidator, PeriodicityHabitValidator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [RelatedOrRewardHabitValidator(),
                      ExecuteTimeHabitValidator(),
                      RelatedIsPleasantHabitValidator(),
                      PleasantHabitValidator(),
                      PeriodicityHabitValidator()]
