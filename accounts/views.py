# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from products.models import Product
from cart.models import Cart

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, request, f'Welcome {username}! Your account has been successfully created. You can now log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def home(request):
    products = Product.objects.all()[:10]  
    return render(request, 'home.html', {'products': products})
