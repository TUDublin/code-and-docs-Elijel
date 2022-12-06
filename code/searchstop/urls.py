from django.urls import path
from . import views

app_name = 'searchstop'

urlpatterns  = [
    path('search/', views.searchResult, name='searchResult'),
]