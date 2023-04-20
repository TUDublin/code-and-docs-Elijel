from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('destinationresults/', views.destination, name='destination'),
    path('destinationsearch/', views.destinationsearch, name='destinationsearch'),
    path('routes/', views.allRoutes, name='allRoutes'),
    path('routes/<route_id>/', views.routeDetails, name='routeDetails'),
    path('allstops/', views.allStops, name='allStops'),
    path('', views.home, name='home'),
    path('nearbystops/', views.nearby_stops, name='nearby_stops'),
    path('<stop_id>/', views.allStopTimes, name='stops_by_stoptimes'),
    path('test/', views.test, name='test'),
]
