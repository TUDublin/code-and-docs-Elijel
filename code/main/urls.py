from django.urls import path
#from .views import HomePageView
from . import views

app_name='main'

urlpatterns = [
    path('', views.home, name='home'),
    path('allstops/', views.allStops, name='allStops'),
    path('nearbystops/', views.nearby_stops, name='nearby_stops'),
    path('<stop_id>/', views.allStopTimes, name='stops_by_stoptimes'),
    path('test/', views.test, name='test'),
]