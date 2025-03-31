from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='index'),
    path('<int:movie_id>/', views.movie_detail, name='detail'),
    path('watch/<int:movie_id>/', views.watch_movie, name='watch'),
    path('trailers/', views.trailer_list, name='trailers'),
]