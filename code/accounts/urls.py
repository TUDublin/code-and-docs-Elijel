from django.urls import path
from main import views
from .views import signupView, signinView, signoutView, favoriteStops

urlpatterns = [
    path('create/', signupView, name='signup'),
    path('login/', signinView, name='signin'),
    path('logout/', signoutView, name='signout'),
    path('favorites/', favoriteStops, name='favoriteStops'),
]
