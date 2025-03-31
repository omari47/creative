from django.urls import path
from . import api_views

urlpatterns = [
    # User API
    path('user/', api_views.user_info, name='user_info'),

    # Movies and trailers API
    path('trailers/', api_views.trailers_list, name='trailers_list'),
    path('movies/', api_views.movies_list, name='movies_list'),
    path('movies/featured/', api_views.featured_movie, name='featured_movie'),
    path('movies/<int:movie_id>/', api_views.movie_detail, name='movie_detail'),

    # Portfolio API
    path('portfolio/', api_views.portfolio_list, name='portfolio_list'),
    path('portfolio/categories/', api_views.categories_list, name='categories_list'),
    path('portfolio/category/<slug:category_slug>/', api_views.portfolio_by_category, name='portfolio_by_category'),
    path('portfolio/<int:item_id>/', api_views.portfolio_detail, name='portfolio_detail'),

    # Workshops API
    path('workshops/', api_views.workshops_list, name='workshops_list'),
    path('workshops/<int:workshop_id>/', api_views.workshop_detail, name='workshop_detail'),

    # Newsletter API
    path('newsletter/subscribe/', api_views.newsletter_subscribe, name='api_newsletter_subscribe'),
]