from django.urls import path
from accounts.views import signupView, signinView, signoutView, addFavoriteView, deleteFavoriteView, favoritesView

urlpatterns = [
    path('create/', signupView, name='signup'),
    path('login/', signinView, name='signin'),
    path('logout/', signoutView, name='signout'),
    path('favorites/add/<str:stop_id>/', addFavoriteView, name='addFavoriteView'),
    path('favorites/delete/<int:pk>/', deleteFavoriteView, name='deleteFavoriteView'),
    path('favorites/', favoritesView, name='favoritesView')
]
