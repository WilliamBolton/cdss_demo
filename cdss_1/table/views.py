from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Vitals_table
import csv
import pandas as pd
from patients.models import Patient
# Create your views here.
# request handler takes request and returns response (i.e., does an action)
#def index(request):
#    return render(request, 'index.html', {'vitals_table': Vitals_table})
#    #return HttpResponse("Hello, world. You're at the tables index.")

def vitals_table_view(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    # Read CSV file into a pandas DataFrame if available
    vitals_data = None
    if patient.csv_file:
        vitals_data = pd.read_csv(patient.csv_file.path)
    return render(request, 'index.html', {'patient': patient, 'vitals_data': vitals_data})

