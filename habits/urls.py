from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitPublicListAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitsConfig.name


urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('public/', HabitPublicListAPIView.as_view(), name='habit_public'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_retrieve'),
    path('<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit_delete'),
]
