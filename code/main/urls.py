from django.urls import path
#from .views import HomePageView
from . import views

app_name='main'

urlpatterns = [
    path('', views.allStops, name='allStops'),
    path('test/', views.home, name='home'),
    path('<stop_id>/', views.allStopTimes, name='stops_by_stoptimes'),
]