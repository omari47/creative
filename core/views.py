from django.utils import timezone

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from movies.models import Movie, Trailer
from portfolio.models import PortfolioItem, Category
from workshops.models import Workshop
from payments.models import NewsletterSubscription

#
# def home(request):
#     """Home page view with all sections"""
#     trailers = Trailer.objects.all()[:8]
#     featured_movie = Movie.objects.filter(is_featured=True).first()
#     portfolio_items = PortfolioItem.objects.all()[:6]
#     categories = Category.objects.all()
#     workshops = Workshop.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
#
#     # Stats for about section
#     stats = [
#         {'value': '8+', 'label': 'Years Experience'},
#         {'value': '200+', 'label': 'Projects Completed'},
#         {'value': '25+', 'label': 'Awards Won'},
#         {'value': '15+', 'label': 'Team Members'}
#     ]
#
#     context = {
#         'trailers': trailers,
#         'featured_movie': featured_movie,
#         'portfolio_items': portfolio_items,
#         'categories': categories,
#         'workshops': workshops,
#         'stats': stats,
#     }
#     return render(request, 'core/home.html', context)
#
# Update your core/views.py
from django.shortcuts import render
from django.utils import timezone
from workshops.models import Workshop
from movies.models import Movie, Trailer
from portfolio.models import PortfolioItem, Category


def home(request):
    # Get workshops (ensure timezone is properly imported)
    workshops = Workshop.objects.all().order_by('date')[:3]  # Remove the date filter for now

    # Get other data as needed
    featured_movie = Movie.objects.filter(is_featured=True).first()
    trailers = Trailer.objects.all()[:6]
    portfolio_items = PortfolioItem.objects.all()[:6]
    categories = Category.objects.all()

    context = {
        'workshops': workshops,
        'featured_movie': featured_movie,
        'trailers': trailers,
        'portfolio_items': portfolio_items,
        'categories': categories,
    }

    # Print debug info to console
    print(f"Debug: Found {workshops.count()} workshops")
    for workshop in workshops:
        print(f"Workshop: {workshop.title}, Date: {workshop.date}")

    return render(request, 'core/home.html', context)
def about(request):
    """About page view"""
    # Stats for about section
    stats = [
        {'value': '8+', 'label': 'Years Experience'},
        {'value': '200+', 'label': 'Projects Completed'},
        {'value': '25+', 'label': 'Awards Won'},
        {'value': '15+', 'label': 'Team Members'}
    ]

    context = {
        'stats': stats,
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Here you would typically send an email
        # For now, just show a success message
        messages.success(request, 'Your message has been sent. We will get back to you soon!')
        return redirect('core:contact')

    return render(request, 'core/contact.html')


@csrf_exempt
def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email', '')

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})

        # Check if already subscribed
        if NewsletterSubscription.objects.filter(email=email).exists():
            return JsonResponse({'success': True, 'message': 'You are already subscribed to our newsletter!'})

        # Save new subscription
        NewsletterSubscription.objects.create(email=email)
        return JsonResponse({'success': True, 'message': 'Thank you for subscribing to our newsletter!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})