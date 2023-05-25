from django.urls import path
from .views import HomePageView, your_view , add_to_favorites

urlpatterns = [

path('', your_view, name='my_model_list'),
    path('home/', HomePageView.as_view(), name='home'),
    path('add_to_favorites/<int:house_id>/', add_to_favorites, name='add_to_favorites'),

   
]


