from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import UserRegistrationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = request.POST.get('remember_me')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # If remember_me is not checked, expire session when browser closes
                if not remember_me:
                    request.session.set_expiry(0)

                # For AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})

                next_url = request.POST.get('next', '/')
                return redirect(next_url)

        # For AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': 'Invalid username or password.'
            })

    # If GET request, show login form (which is now handled in base template)
    return redirect('core:home')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # For AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            next_url = request.POST.get('next', '/')
            return redirect(next_url)

        # For AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = ' '.join([error[0] for field, error in form.errors.items()])
            return JsonResponse({
                'success': False,
                'errors': errors
            })

    # If GET request, show registration form (which is now handled in base template)
    return redirect('core:home')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('core:home')
# # API views
#
# def api_login(request):
#     """API login endpoint"""
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#
#     try:
#         data = json.loads(request.body)
#         username = data.get('username', '')
#         password = data.get('password', '')
#
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#             })
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=401)
#
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)
#
#
# @csrf_exempt
# def api_register(request):
#     """API register endpoint"""
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#
#     try:
#         data = json.loads(request.body)
#         form = UserRegisterForm(data)
#
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return JsonResponse({
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#             })
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)
#
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)
#
#
# @login_required
# def api_logout(request):
#     """API logout endpoint"""
#     logout(request)
#     return JsonResponse({'success': True})