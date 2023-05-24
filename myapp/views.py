from django.views.generic import ListView
from .models import MyModel , House
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator
import json
class HomePageView(TemplateView):
     template_name="my_model_list.html"
@staticmethod
def your_view(request): 
        print("Your view function called")
        data = House.objects.all()
        paginator = Paginator(data, 10)  # Specify the number of items per page

        page_number = request.GET.get('page')  # Get the current page number from the request
        page_obj = paginator.get_page(page_number)  # Get the Page object for the current page

        return render(request, 'my_model_list.html', {'page_obj': page_obj})
        #return render(request, 'my_model_list.html', {'data': data})



