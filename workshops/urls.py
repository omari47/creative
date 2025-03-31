from django.urls import path
from . import views

app_name = 'workshops'

urlpatterns = [
    path('', views.workshop_list, name='index'),
    path('<int:workshop_id>/', views.workshop_detail, name='detail'),
    path('register/<int:workshop_id>/', views.register_workshop, name='register'),
    path('cancel/<int:workshop_id>/', views.cancel_registration, name='cancel'),
    path('my-workshops/', views.my_workshops, name='my_workshops'),
]