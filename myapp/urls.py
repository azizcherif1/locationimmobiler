from django.urls import path
from .views import HomePageView, your_view 
urlpatterns = [

path('', your_view, name='my_model_list'),
    path('home/', HomePageView.as_view(), name='home'),
]