from django.shortcuts import render
from django.http import HttpResponse
from .models import Vitals_table
import csv
# Create your views here.
# request handler takes request and returns response (i.e., does an action)
#def index(request):
#    return render(request, 'index.html', {'vitals_table': Vitals_table})
#    #return HttpResponse("Hello, world. You're at the tables index.")

def vitals_table_view(request):
    vitals_data = Vitals_table.objects.all()
    return render(request, 'table/templates/index.html', {'vitals_data': vitals_data})

