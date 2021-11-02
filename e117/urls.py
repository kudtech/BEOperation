
from django.urls import path, include
from .views import *
app_name = 'e117'

urlpatterns = [
    path('create/', SaveJob.as_view(), name='job-create')  
]
