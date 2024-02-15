import csv
import os
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from .models import Patient
import json
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.http import JsonResponse
from .models import LinkClick

def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    # Call the function to create test user profiles
    #User.objects.all().delete()
    #create_test_user_profiles()
    
    print_bool = False
    print_bool = True
    if print_bool == True:
        # Retrieve all UserProfile instances
        user_profiles = UserProfile.objects.all()
        # Print or iterate over the user profiles
        for user_profile in user_profiles:
            print(user_profile.id_value, user_profile.archetype)
        print('\n\n\n')

    if request.method == 'POST':
        id_value = request.POST['id_value']
        archetype = request.POST['archetype']
        password = 'test_password'
        try:
            # Authenticate the user
            user = authenticate(request, username=id_value, password=password)
            print('user:', user)
            print('archetype:', archetype)
            if user is not None:
                login(request, user)

                # Create or update user profile
                #profile = UserProfile.objects.create(id_value=id_value, archetype=archetype)
                profile, created = UserProfile.objects.get_or_create(user=user, id_value=id_value, archetype=archetype)
                profile.save()

                return redirect('patient_list')
            
        except:
            # Handle the case where UserProfile does not exist
            messages.error(request, 'Invalid ID or Archetype combination. Please try again.')
            return redirect('/')  # Redirect back to the login page
    
    return render(request, 'patients/login.html')

@login_required(login_url='/')
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required(login_url='/')
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    print('patient_id:', patient_id)

    # Read CSV file and put in JSON format if available
    if patient.vitals_csv_path == 'nan':
        vitals_data = None
        vitals_data_json = None
    else:
        vitals_data = pd.read_csv(patient.vitals_csv_path)
        #vitals_data = vitals_data.to_json(orient='records')
        vitals_data_dict = vitals_data.to_dict(orient='records')
        vitals_data_json = json.dumps(vitals_data_dict)
        #print(vitals_data_json)
        #print(type(vitals_data_json))

    # Accessing the logged-in user's UserProfile
    user_profile = request.user.userprofile
    user_archetype = user_profile.archetype
    print('user_archetype:', user_archetype)

    # Get the apropriate template
    template = get_template_fun(patient_id, user_archetype)
    print('template:', template)

    return render(request, template, {
        'patient': patient, 
        'vitals_data_json': vitals_data_json, 
        'has_vitals_data': vitals_data is not None,
        })

def prediction_page(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    if patient.patient_csv_path == 'nan':
        patient_data = None
        patient_data_json = None
    else:
        patient_data = pd.read_csv(patient.patient_csv_path)
        patient_dict = patient_data.to_dict(orient='records')
        patient_data_json = json.dumps(patient_dict)

    if patient.similar_patients_csv_path == 'nan':
        similar_patients_data = None
        similar_patients_data_json = None
    else:
        similar_patients_data = pd.read_csv(patient.similar_patients_csv_path)
        similar_patients_dict = similar_patients_data.to_dict(orient='records')
        similar_patients_data_json = json.dumps(similar_patients_dict)
    
    if patient.feature_similarity_path == 'nan':
        image_path = None
    else:
        image_path = patient.feature_similarity_path
        # Strip to allow for loading in html
        image_path = image_path.lstrip('images/')
    
    # Define llm summary
    positive_points = llm_positive_fun(patient.name)
    negative_points = llm_negative_fun(patient.name)

    return render(request, 'patients/prediction_page.html', {
        'patient': patient,
        'patient_data_json': patient_data_json, 
        'has_patient_data': patient_data is not None,
        'similar_patients_data_json': similar_patients_data_json, 
        'has_similar_patients_data': similar_patients_data is not None,
        'image_path': image_path,
        'positive_points': positive_points,
        'negative_points': negative_points,
        })

def guideline_page(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    # Define llm summary
    decision_logic = decision_logic_fun(patient.name)

    # Define llm summary
    decision_outcome = decision_outcome_fun(patient.name)
    print(decision_outcome)

    return render(request, 'patients/guideline_page.html', {
        'patient': patient, 
        'decision_logic': decision_logic, 
        'decision_outcome': decision_outcome})

def process_user_input(request, patient_id):
    #print('hi')
    if request.method == 'POST':
        # Update patient.form_filled_in
        patient = get_object_or_404(Patient, pk=patient_id)
        patient.form_filled_in = True
        patient.save()

        # Get the user input from the form
        switch_choice = request.POST.get('switch_choice')
        explanation = request.POST.get('explanation')

        # Accessing the logged-in user's UserProfile
        user_profile = request.user.userprofile
        user_archetype = user_profile.archetype
        user_id = user_profile.id_value

        # Process the user input (you can save it to the database or perform other actions)
        # For demonstration purposes, we'll just print the input
        print(f"user_id: {user_id}, user_archetype: {user_archetype}")
        print(f"patient_id: {patient_id}, Switch Choice: {switch_choice}, Explanation: {explanation}")

        # Save choices to a CSV file
        csv_file_path = f'/home/wb1115/VSCode_projects/cdss/cdss_1/cdss_1/switch_results/patient_{patient_id}_choices.csv'
        #csv_file_path = os.path.join(os.path.dirname(), f'../csv_results/patient_{patient_id}_choices.csv')
        #print(csv_file_path)
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['user_id', 'user_archetype', 'switch_choice', 'explanation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Check if the CSV file is empty and write headers if needed
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'user_id': user_id, 'user_archetype': user_archetype, 'switch_choice': switch_choice, 'explanation': explanation})

        # Redirect back to the patient details page
        return redirect('patient_list')
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)

def track_link_click(request):
    print('request.body:', request.body)
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = json.loads(request.body)
        link_id = data.get('linkId', None)
        patient_id = data.get('patientId', None)

        print('link_id:', data)
        print('patient_id:', patient_id)

        # Record link click in the database
        if link_id:
            print('Creating LinkClick object')
            LinkClick.objects.create(link_id=link_id, user=request.user,  patient_id=patient_id)

        return JsonResponse({'message': 'link click recorded successfully'})
    print('message,', 'Invalid request')
    return JsonResponse({'message': 'Invalid request'}, status=400)
    
def llm_positive_fun(n):
    if n == 'Patient 1':
        return [
        "The model correctly predicts the decision for similar examples",
        "Features are relativly similar between the patient in question and the similar patients",
        ]
    elif n == 'Patient 2':
        return 'Switch'
    else:
        return 'nan'
    
def llm_negative_fun(n):
    if n == 'Patient 1':
        return [
        "A negative point is that there are some diferences between the patient in question and similar patients (e.g., age and co-morbidities)",
        "This is another point",
        ]
    elif n == 'Patient 2':
        return 'Switch'
    else:
        return 'nan'

def decision_logic_fun(n):
    if n == 'Patient 1':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['No']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['No']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        ]
    elif n == 'Patient 2':
        return 'Switch'
    else:
        return 'nan'

def decision_outcome_fun(n):
    if n == 'Patient 1':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    elif n == 'Patient 2':
        return [{'label': 'Switch', 'answers': ['XXX']}]
    else:
        return 'nan'

def get_template_fun(patient_id, user_archetype):
    if patient_id == 2 and user_archetype == 'a':
        return 'patients/patient_detail_simple.html'
    elif patient_id == 4 and user_archetype == 'a':
        return 'patients/patient_detail_simple.html'
    else:
        return 'patients/patient_detail.html'
