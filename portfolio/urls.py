from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_list, name='index'),
    path('<int:item_id>/', views.portfolio_detail, name='detail'),
]