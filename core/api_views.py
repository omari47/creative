from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

from movies.models import Movie, Trailer
from portfolio.models import PortfolioItem, Category
from workshops.models import Workshop
from payments.models import NewsletterSubscription


# User API
@login_required
def user_info(request):
    """Get current user information"""
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number,
        'profile_image': user.profile_image.url if user.profile_image else None,
    }
    return JsonResponse(data)


# Movies and trailers API
def trailers_list(request):
    """Get list of trailers"""
    trailers = Trailer.objects.all()
    data = [{
        'id': trailer.id,
        'title': trailer.title,
        'description': trailer.description,
        'trailer_url': trailer.trailer_url,
        'image_url': trailer.image.url,
        'movie_id': trailer.movie.id if trailer.movie else None,
    } for trailer in trailers]
    return JsonResponse(data, safe=False)


def movies_list(request):
    """Get list of movies"""
    movies = Movie.objects.all()
    data = [{
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'categories': movie.categories,
        'price': float(movie.price),
        'duration': movie.duration,
        'rating': float(movie.rating),
        'trailer_url': movie.trailer_url,
        'video_url': movie.video_url,
        'image_url': movie.image.url,
        'is_featured': movie.is_featured,
    } for movie in movies]
    return JsonResponse(data, safe=False)


def featured_movie(request):
    """Get featured movie"""
    movie = Movie.objects.filter(is_featured=True).first()
    if not movie:
        return JsonResponse({}, status=404)

    data = {
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'categories': movie.categories,
        'price': float(movie.price),
        'duration': movie.duration,
        'rating': float(movie.rating),
        'trailer_url': movie.trailer_url,
        'video_url': movie.video_url,
        'image_url': movie.image.url,
    }
    return JsonResponse(data)


def movie_detail(request, movie_id):
    """Get movie details"""
    try:
        movie = Movie.objects.get(id=movie_id)
        data = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'categories': movie.categories,
            'price': float(movie.price),
            'duration': movie.duration,
            'rating': float(movie.rating),
            'trailer_url': movie.trailer_url,
            'video_url': movie.video_url,
            'image_url': movie.image.url,
            'is_featured': movie.is_featured,
        }
        return JsonResponse(data)
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)


# Portfolio API
def portfolio_list(request):
    """Get list of portfolio items"""
    items = PortfolioItem.objects.all()
    data = [{
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'category': item.category.name,
        'category_slug': item.category.slug,
        'image_url': item.image.url,
    } for item in items]
    return JsonResponse(data, safe=False)


def categories_list(request):
    """Get list of portfolio categories"""
    categories = Category.objects.all()
    data = [{
        'id': category.id,
        'name': category.name,
        'slug': category.slug,
    } for category in categories]
    return JsonResponse(data, safe=False)


def portfolio_by_category(request, category_slug):
    """Get portfolio items by category"""
    try:
        category = Category.objects.get(slug=category_slug)
        items = PortfolioItem.objects.filter(category=category)
        data = [{
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'category': item.category.name,
            'image_url': item.image.url,
        } for item in items]
        return JsonResponse(data, safe=False)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)


def portfolio_detail(request, item_id):
    """Get portfolio item details"""
    try:
        item = PortfolioItem.objects.get(id=item_id)
        data = {
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'category': item.category.name,
            'category_slug': item.category.slug,
            'image_url': item.image.url,
        }
        return JsonResponse(data)
    except PortfolioItem.DoesNotExist:
        return JsonResponse({'error': 'Portfolio item not found'}, status=404)


# Workshops API
def workshops_list(request):
    """Get list of workshops"""
    workshops = Workshop.objects.all()
    data = [{
        'id': workshop.id,
        'title': workshop.title,
        'description': workshop.description,
        'price': float(workshop.price),
        'date': workshop.date.isoformat(),
        'location': workshop.location,
        'tags': workshop.tags,
        'seats_available': workshop.seats_available,
        'image_url': workshop.image.url,
    } for workshop in workshops]
    return JsonResponse(data, safe=False)


def workshop_detail(request, workshop_id):
    """Get workshop details"""
    try:
        workshop = Workshop.objects.get(id=workshop_id)
        data = {
            'id': workshop.id,
            'title': workshop.title,
            'description': workshop.description,
            'price': float(workshop.price),
            'date': workshop.date.isoformat(),
            'location': workshop.location,
            'tags': workshop.tags,
            'seats_available': workshop.seats_available,
            'image_url': workshop.image.url,
        }
        return JsonResponse(data)
    except Workshop.DoesNotExist:
        return JsonResponse({'error': 'Workshop not found'}, status=404)


# Newsletter API
@csrf_exempt
def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email', '')

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

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)