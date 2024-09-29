from django.urls import path
from .views import *

app_name = 'summary_of_the_day'

urlpatterns = [
    path('', index, name='summary_of_the_day_index'),
    path('cigarettes/', cigarettes, name='summary_of_the_day_cigarettes'),
    path('pull-ups/', pullups, name='summary_of_the_day_pullups'),
    path('cigarettes/stat', cigarettes_stat,
         name='summary_of_the_day_cigarettes_stat'),
]
