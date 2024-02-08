import csv
import os
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from .models import Patient
import json
from django.http import HttpResponse

# Create your views here.

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    print(patient_id)

    # Read CSV file into a pandas DataFrame if available
    if patient.csv_path == 'nan':
        vitals_data = None
        vitals_data_json = None
    else:
        vitals_data = pd.read_csv(patient.csv_path)
        #vitals_data = vitals_data.to_json(orient='records')
        vitals_data_dict = vitals_data.to_dict(orient='records')
        vitals_data_json = json.dumps(vitals_data_dict)
        #print(vitals_data_json)
        #print(type(vitals_data_json))
    return render(request, 'patients/patient_detail.html', {
        'patient': patient, 
        'vitals_data_json': vitals_data_json, 
        'has_vitals_data': vitals_data is not None})

def prediction_page(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    return render(request, 'patients/prediction_page.html', {'patient': patient})

def guideline_page(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    return render(request, 'patients/guideline_page.html', {'patient': patient})

def process_user_input(request, patient_id):
    print('hi')
    if request.method == 'POST':
        # Get the user input from the form
        switch_choice = request.POST.get('switch_choice')
        explanation = request.POST.get('explanation')

        # Process the user input (you can save it to the database or perform other actions)
        # For demonstration purposes, we'll just print the input
        print(f"patient_id: {patient_id}, Switch Choice: {switch_choice}, Explanation: {explanation}")

        # Save choices to a CSV file
        csv_file_path = f'/home/wb1115/VSCode_projects/cdss/cdss_1/cdss_1/csv_results/patient_{patient_id}_choices.csv'
        #csv_file_path = os.path.join(os.path.dirname(), f'../csv_results/patient_{patient_id}_choices.csv')
        print(csv_file_path)
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['Switch Choice', 'Explanation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Check if the CSV file is empty and write headers if needed
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Switch Choice': switch_choice, 'Explanation': explanation})

        # Redirect back to the patient details page
        return redirect('patient_list')
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405) 