from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from payments.models import Payment


@csrf_exempt
def register_view(request):
    """Register a new user"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('core:home')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@csrf_exempt
def login_view(request):
    """Login a user"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout a user"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)

    # Get user's payments
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'form': form,
        'payments': payments,
    }
    return render(request, 'accounts/profile.html', context)


# API views
@csrf_exempt
def api_login(request):
    """API login endpoint"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@csrf_exempt
def api_register(request):
    """API register endpoint"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        form = UserRegisterForm(data)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required
def api_logout(request):
    """API logout endpoint"""
    logout(request)
    return JsonResponse({'success': True})