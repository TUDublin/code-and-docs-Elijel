from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .models import CustomUser, Favorite
from main.models import Stop
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect
@login_required
def favoritesView(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required
def addFavoriteView(request, stop_id):
    user = request.user
    stop = get_object_or_404(Stop, stop_id=stop_id)
    
    if Favorite.objects.filter(user=user, stop=stop).exists():
        return redirect('favoritesView')
    
    favorite = Favorite(user=user, stop=stop)
    favorite.save()
    return redirect('favoritesView')

@login_required
def deleteFavoriteView(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk, user=request.user)
    favorite.delete()
    return redirect("favoritesView")

def signupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = CustomUser.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form':form})

def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form':form})

def signoutView(request):
    logout(request)
    return redirect('signin')
