from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from .models import Movie, Trailer
from payments.models import Payment


def movie_list(request):
    """View all movies"""
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies/movie_list.html', context)

#
# def movie_detail(request, movie_id):
#     """View a specific movie details"""
#     movie = get_object_or_404(Movie, id=movie_id)
#
#     # Check if user has paid for this movie
#     has_paid = False
#     if request.user.is_authenticated:
#         has_paid = Payment.objects.filter(
#             user=request.user,
#             movie=movie,
#             status='completed'
#         ).exists()
#
#     context = {
#         'movie': movie,
#         'has_paid': has_paid,
#     }
#     return render(request, 'movies/movie_detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Movie

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})
@login_required
def watch_movie(request, movie_id):
    """Watch a movie (requires payment)"""
    movie = get_object_or_404(Movie, id=movie_id)

    # Check if user has paid for this movie
    has_paid = Payment.objects.filter(
        user=request.user,
        movie=movie,
        status='completed'
    ).exists()

    if not has_paid:
        messages.error(request, 'You need to purchase this movie before watching it.')
        return redirect('payments:process', movie_id=movie_id)

    context = {'movie': movie}
    return render(request, 'movies/watch_movie.html', context)


def trailer_list(request):
    """View all trailers"""
    trailers = Trailer.objects.all()
    context = {'trailers': trailers}
    return render(request, 'movies/trailer_list.html', context)