import csv
import os
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from .models import ParticipantInfo, Patient, Patient_demo
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
from django.views.decorators.csrf import csrf_exempt
from .models import HoverEvent

def logout_view(request):
    logout(request)
    return redirect('/')

def thank_you(request):
    return render(request, 'patients/thank_you.html')  

def login_view(request):
    # Call the function to create test user profiles
    #User.objects.all().delete()
    #create_test_user_profiles()
    
    #print_bool = False
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

        if id_value == 'demo':
            try:
                # Authenticate the demo user
                user = authenticate(request, username=id_value, password=password)
                print('user:', user)
                print('archetype:', archetype)
                if user is not None:
                    login(request, user)
                    # Create or update user profile
                    #profile = UserProfile.objects.create(id_value=id_value, archetype=archetype)
                    profile, created = UserProfile.objects.get_or_create(user=user, id_value=id_value, archetype=archetype)
                    profile.save()
                    return redirect('patient_list_demo')  # Redirect to the demo dashboard
            except:
                # Handle the case where UserProfile does not exist
                print('Invalid ID or Archetype combination. Please try again.')
                messages.error(request, 'Invalid ID or Archetype combination. Please try again.')
                return redirect('/')  # Redirect back to the login page

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

                return redirect('details')
            
        except:
            # Handle the case where UserProfile does not exist
            print('Invalid ID or Archetype combination. Please try again.')
            messages.error(request, 'Invalid ID or Archetype combination. Please try again.')
            return redirect('/')  # Redirect back to the login page
    
    return render(request, 'patients/login.html')

@login_required(login_url='/')
def details(request):
    if request.method == 'POST':
        age = request.POST['age']
        sex = request.POST['sex']
        medical_speciality = request.POST['medical_speciality']
        grade = request.POST['grade']
        # Accessing the logged-in user's info
        user = request.user.userprofile
        user_id = user.id_value
        user_archetype = user.archetype

        # Save detials to a CSV file
        csv_file_path = f'/home/wb1115/VSCode_projects/cdss/cdss_1/cdss_1/demographic_results/demographics.csv'
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['user_id', 'user_archetype', 'age', 'sex', 'medical_speciality', 'grade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Check if the CSV file is empty and write headers if needed
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'user_id': user_id, 'user_archetype': user_archetype, 'age':age, 'sex':sex, 'medical_speciality':medical_speciality, 'grade':grade})
        
        return redirect('patient_list')
    else:
        return render(request, 'patients/details.html')

@login_required(login_url='/')
def patient_list(request):
    patients = Patient.objects.all()
    #print('patients', patients)
    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required(login_url='/')
def patient_list_demo(request):
    patients_demo = Patient_demo.objects.all()
    #print('patients_demo', patients_demo)
    return render(request, 'patients/patient_list_demo.html', {'patients': patients_demo})

@login_required(login_url='/')
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    print('patient_id:', patient_id)

    # Read CSV file and put in JSON format if available
    if patient.vitals_csv_path == 'nan':
        vitals_data = None
        vitals_data_json = None
        vitals_data_no_nan_json = None
    else:
        vitals_data = pd.read_csv(patient.vitals_csv_path)
        vitals_data_no_nan = vitals_data.fillna('')
        vitals_data_no_nan = vitals_data_no_nan.astype(str) # Conver to strings to preserve dp
        #print(vitals_data)
        #print(vitals_data_no_nan)
        #vitals_data = vitals_data.to_json(orient='records')
        vitals_data_dict = vitals_data.to_dict(orient='records')
        vitals_data_no_nan_dict = vitals_data_no_nan.to_dict(orient='records')
        #print(vitals_data_dict)
        #print(vitals_data_no_nan_dict)
        vitals_data_json = json.dumps(vitals_data_dict)
        vitals_data_no_nan_json = json.dumps(vitals_data_no_nan_dict)
        #print(vitals_data_json)
        #print(vitals_data_no_nan_json)
        #print(type(vitals_data_json))

    print(patient.comorbidities)
    print(type(patient.comorbidities))
    print(patient.imddecil)
    print(type(patient.imddecil))
    print(patient.diagnosis)
    print(type(patient.diagnosis))

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
        'vitals_data_no_nan_json': vitals_data_no_nan_json, 
        'has_vitals_data': vitals_data is not None,
        })

@login_required(login_url='/')
def patient_detail_demo(request, patient_id):
    patient = get_object_or_404(Patient_demo, pk=patient_id)
    print('patient_id:', patient_id)

    # Read CSV file and put in JSON format if available
    if patient.vitals_csv_path == 'nan':
        vitals_data = None
        vitals_data_json = None
        vitals_data_no_nan_json = None
    else:
        vitals_data = pd.read_csv(patient.vitals_csv_path)
        vitals_data_no_nan = vitals_data.fillna('')
        vitals_data_no_nan = vitals_data_no_nan.astype(str) # Conver to strings to preserve dp
        #print(vitals_data)
        #print(vitals_data_no_nan)
        #vitals_data = vitals_data.to_json(orient='records')
        vitals_data_dict = vitals_data.to_dict(orient='records')
        vitals_data_no_nan_dict = vitals_data_no_nan.to_dict(orient='records')
        #print(vitals_data_dict)
        #print(vitals_data_no_nan_dict)
        vitals_data_json = json.dumps(vitals_data_dict)
        vitals_data_no_nan_json = json.dumps(vitals_data_no_nan_dict)
        #print(vitals_data_json)
        #print(vitals_data_no_nan_json)
        #print(type(vitals_data_json))

    # Accessing the logged-in user's UserProfile
    user_profile = request.user.userprofile
    user_archetype = user_profile.archetype
    print('user_archetype:', user_archetype)

    # Get the apropriate template
    template = get_template_fun_demo(patient_id, user_archetype)
    print('template:', template)

    return render(request, template, {
        'patient': patient, 
        'vitals_data_json': vitals_data_json,
        'vitals_data_no_nan_json': vitals_data_no_nan_json, 
        'has_vitals_data': vitals_data is not None,
        })

@login_required(login_url='/')
def prediction_page(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    if patient.patient_csv_path == 'nan':
        patient_data = None
        patient_data_json = None
    else:
        patient_data = pd.read_csv(patient.patient_csv_path, keep_default_na=False)
        patient_data = patient_data.astype(str) # Conver to strings to preserve dp
        patient_dict = patient_data.to_dict(orient='records')
        patient_data_json = json.dumps(patient_dict)

    if patient.similar_patients_csv_path == 'nan':
        similar_patients_data = None
        similar_patients_data_json = None
    else:
        similar_patients_data = pd.read_csv(patient.similar_patients_csv_path, keep_default_na=False)
        similar_patients_data = similar_patients_data.astype(str) # Conver to strings to preserve dp
        similar_patients_dict = similar_patients_data.to_dict(orient='records')
        similar_patients_data_json = json.dumps(similar_patients_dict)
    
    if patient.feature_similarity_path == 'nan':
        image_path = None
    else:
        print(patient.feature_similarity_path)
        image_path = patient.feature_similarity_path
        # Strip to allow for loading in html
        image_path = image_path.lstrip('images/')
    
    # Define llm summary
    llm_points = llm_fun(patient.name)

    return render(request, 'patients/prediction_page.html', {
        'patient': patient,
        'patient_data_json': patient_data_json, 
        'has_patient_data': patient_data is not None,
        'similar_patients_data_json': similar_patients_data_json, 
        'has_similar_patients_data': similar_patients_data is not None,
        'image_path': image_path,
        'llm_points': llm_points,
        })

@login_required(login_url='/')
def prediction_page_demo(request, patient_id):
    patient = get_object_or_404(Patient_demo, pk=patient_id)

    if patient.patient_csv_path == 'nan':
        patient_data = None
        patient_data_json = None
    else:
        patient_data = pd.read_csv(patient.patient_csv_path, keep_default_na=False)
        patient_data = patient_data.astype(str) # Conver to strings to preserve dp
        patient_dict = patient_data.to_dict(orient='records')
        patient_data_json = json.dumps(patient_dict)

    if patient.similar_patients_csv_path == 'nan':
        similar_patients_data = None
        similar_patients_data_json = None
    else:
        similar_patients_data = pd.read_csv(patient.similar_patients_csv_path, keep_default_na=False)
        similar_patients_data = similar_patients_data.astype(str) # Conver to strings to preserve dp
        similar_patients_dict = similar_patients_data.to_dict(orient='records')
        similar_patients_data_json = json.dumps(similar_patients_dict)
    
    if patient.feature_similarity_path == 'nan':
        image_path = None
    else:
        image_path = patient.feature_similarity_path
        # Strip to allow for loading in html
        image_path = image_path.lstrip('images/')
    
    # Define llm summary
    llm_points = llm_demo_fun(patient.name)

    return render(request, 'patients/prediction_page_demo.html', {
        'patient': patient,
        'patient_data_json': patient_data_json, 
        'has_patient_data': patient_data is not None,
        'similar_patients_data_json': similar_patients_data_json, 
        'has_similar_patients_data': similar_patients_data is not None,
        'image_path': image_path,
        'llm_points': llm_points,
        })

@login_required(login_url='/')
def guideline_page(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    # Define guideline summary
    decision_logic = decision_logic_fun(patient.name)

    # Define guideline summary
    decision_outcome = decision_outcome_fun(patient.name)
    #print(decision_outcome)

    return render(request, 'patients/guideline_page.html', {
        'patient': patient, 
        'decision_logic': decision_logic, 
        'decision_outcome': decision_outcome})

@login_required(login_url='/')
def guideline_page_demo(request, patient_id):
    patient = get_object_or_404(Patient_demo, pk=patient_id)

    # Define guideline summary
    decision_logic = decision_logic_fun_demo(patient.name)

    # Define guideline summary
    decision_outcome = decision_outcome_fun_demo(patient.name)
    print(decision_outcome)

    return render(request, 'patients/guideline_page_demo.html', {
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
            print('Saved!')

        # Redirect back to the patient details page
        return redirect('patient_list')
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)

def process_user_input_demo(request, patient_id):
    print('Demo input - not saved')
    if request.method == 'POST':
        # Update patient.form_filled_in
        patient = get_object_or_404(Patient_demo, pk=patient_id)
        patient.form_filled_in = True
        patient.save()
    
    # Redirect back to the patient details page
        return redirect('patient_list_demo')
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)

def track_link_click(request):
    #print('request.body:', request.body)
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = json.loads(request.body)
        link_id = data.get('linkId', None)
        patient_id = data.get('patientId', None)

        #print('link_id:', data)
        #print('patient_id:', patient_id)

        # Record link click in the database
        if link_id:
            print('Creating LinkClick object')
            LinkClick.objects.create(link_id=link_id, user=request.user,  patient_id=patient_id)

        return JsonResponse({'message': 'link click recorded successfully'})
    
    print('message,', 'Invalid request')
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def record_hover_event(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        component = data.get('component')
        hover_duration = data.get('hover_duration')
        patient_id = data.get('patientId', None)

        print('Creating HoverEvent object')
        # Save the hover event to the database
        HoverEvent.objects.create(
            user=request.user,
            component=component,
            hover_duration=hover_duration,
            patient_id=patient_id,
        )

        return JsonResponse({'message': 'hover event recorded successfully'})
    
    print('message,', 'Error')
    return JsonResponse({'message': 'Error'}, status=400)

@csrf_exempt
def save_legend_click(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract data from the request
        legend_name = data.get('legendName')
        patient = data.get('patient')
        timestamp = data.get('timestamp')

        # Accessing the logged-in user's info
        user = request.user.userprofile
        user_id = user.id_value
        user_archetype = user.archetype


        # Save data to a CSV file
        csv_file_path = f'/home/wb1115/VSCode_projects/cdss/cdss_1/cdss_1/legend_click_results/legend_click_results.csv'
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['user_id', 'user_archetype', 'patient', 'variable', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Check if the CSV file is empty and write headers if needed
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'user_id': user_id, 'user_archetype': user_archetype, 'patient': patient, 'variable': legend_name, 'timestamp': timestamp})
        
        print('Legend click data saved')

        return JsonResponse({'message': 'Legend click data saved successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def llm_fun(n):
    if n == 'Patient 1':
        return [
        "The patient has a high index of multiple deprivation (4), indicating significant social disadvantage, which has been linked to poorer health outcomes",
        "The patient's vitals show a greater similarity to patients for whom the AI model predicted that IV treatment should be continued",
        "Three out of the five similar patients had Sepsis as the infecting organism and the AI model predicted that they should not switch from IV to oral antibiotics, which aligns with the prediction for the patient in question",
        ]
    elif n == 'Patient 7':
        return [
        "Feature contribution table shows that SpO2 and Glasgow Coma Score (Motor) features had a negative contribution to switching the patient from IV to oral antibiotics",
        "Three similar patients with the most importance scores (0.82, 0.08 and 0.06) all had the prediction of not switching from IV to oral antibiotics by the AI model, which is consistent with the prediction for the patient in question",
        ]
    else:
        return 'nan'
    
def llm_demo_fun(n):
    if n == 'Patient 1':
        return [
        "Test",
        "Test",
        ]
    else:
        return 'nan'

def decision_logic_fun(n):
    if n == 'Patient 1':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['No']},
        ]
    elif n == 'Patient 2':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['Yes']}
        ]
    elif n == 'Patient 3':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['No']},
        ]
    elif n == 'Patient 4':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['Yes']}
        ]
    elif n == 'Patient 5':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['No']}
        ]
    elif n == 'Patient 6':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['Yes']}
        ]
    elif n == 'Patient 7':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        ]
    elif n == 'Patient 8':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['Yes']}
        ]
    elif n == 'Patient 9':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['Yes']}
        ]
    elif n == 'Patient 10':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['Yes']}
        ]
    elif n == 'Patient 11':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        ]
    elif n == 'Patient 12':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        ]
    else:
        return 'nan'

def decision_outcome_fun(n):
    if n == 'Patient 1':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    elif n == 'Patient 2':
        return [{'label': 'Prompt or assess for switch', 'answers': ['Prescriber or infection specialist to consider IV to oral switch. Identify whether a suitable oral switch option is available, considering for example oral bioavailability, any clinically significant drug interactions, patient allergies or contra-indications']}]
    elif n == 'Patient 3':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    elif n == 'Patient 4':
        return [{'label': 'Prompt or assess for switch', 'answers': ['Prescriber or infection specialist to consider IV to oral switch. Identify whether a suitable oral switch option is available, considering for example oral bioavailability, any clinically significant drug interactions, patient allergies or contra-indications']}]
    elif n == 'Patient 5':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    elif n == 'Patient 6':
        return [{'label': 'Prompt or assess for switch', 'answers': ['Prescriber or infection specialist to consider IV to oral switch. Identify whether a suitable oral switch option is available, considering for example oral bioavailability, any clinically significant drug interactions, patient allergies or contra-indications']}]
    elif n == 'Patient 7':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    elif n == 'Patient 8':
        return [{'label': 'Prompt or assess for switch', 'answers': ['Prescriber or infection specialist to consider IV to oral switch. Identify whether a suitable oral switch option is available, considering for example oral bioavailability, any clinically significant drug interactions, patient allergies or contra-indications']}]
    elif n == 'Patient 9':
        return [{'label': 'Prompt or assess for switch', 'answers': ['Prescriber or infection specialist to consider IV to oral switch. Identify whether a suitable oral switch option is available, considering for example oral bioavailability, any clinically significant drug interactions, patient allergies or contra-indications']}]
    elif n == 'Patient 10':
        return [{'label': 'Prompt or assess for switch', 'answers': ['Prescriber or infection specialist to consider IV to oral switch. Identify whether a suitable oral switch option is available, considering for example oral bioavailability, any clinically significant drug interactions, patient allergies or contra-indications']}]
    elif n == 'Patient 11':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    elif n == 'Patient 12':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    else:
        return 'nan'

def decision_logic_fun_demo(n):
    if n == 'Patient 1':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        ]
    elif n == 'Patient 2':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['Yes']},
        {'label': 'Has the patient’s temperature been between 36-38°C for the past 24 hours?', 'answers': ['Yes']},
        {'label': 'Is the patient’s Early Warning Score (EWS) decreasing?', 'answers': ['Yes']}
        ]
    elif n == 'Patient 3':
        return [
        {'label': 'Does your patient have an infection that may require special consideration?', 'answers': ['No']},
        {'label': 'Is the patient’s gastrointestinal tract functioning with no evidence of malabsorption?', 'answers': ['Yes']},
        {'label': 'Is the patient’s swallow or enteral tube administration safe?', 'answers': ['Yes']},
        {'label': 'Are there any significant concerns over patient adherence to oral treatment?', 'answers': ['No']},
        {'label': 'Has the patient vomited within the last 24 hours?', 'answers': ['No']},
        {'label': 'Are the patient’s clinical signs and symptoms of infection improving?', 'answers': ['No']},
        ]
    else:
        return 'nan'

def decision_outcome_fun_demo(n):
    if n == 'Patient 1':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    elif n == 'Patient 2':
        return [{'label': 'Prompt or assess for switch', 'answers': ['Prescriber or infection specialist to consider IV to oral switch. Identify whether a suitable oral switch option is available, considering for example oral bioavailability, any clinically significant drug interactions, patient allergies or contra-indications']}]
    elif n == 'Patient 3':
        return [{'label': 'Dont switch', 'answers': ['Reassess in 24 hours']}]
    else:
        return 'nan'

def get_template_fun(patient_id, user_archetype):
    # Order of seeing CDSS (1) or SOC (2)
    # a and b are opposites of each other
    # a = 122121122112
    # b = 211212211221
    a_list = [1,2,2,1,2,1,1,2,2,1,1,2]
    b_list = [2,1,1,2,1,2,2,1,1,2,2,1]
    if user_archetype == 'a':
        n = a_list[patient_id-1]
    elif user_archetype == 'b':
        n = b_list[patient_id-1]
    
    if n == 1:
        return 'patients/patient_detail.html'
    elif n == 2:
        return 'patients/patient_detail_simple.html'

    # Old code for initial dev below
    '''if patient_id == 2 and user_archetype == 'a':
        return 'patients/patient_detail_simple.html'
    elif patient_id == 4 and user_archetype == 'a':
        return 'patients/patient_detail_simple.html'
    else:
        return 'patients/patient_detail.html'''

def get_template_fun_demo(patient_id, user_archetype):
    print('patient_id', patient_id)
    print('user_archetype', user_archetype)
    if patient_id == 2 and user_archetype == 'a':
        return 'patients/patient_detail_simple_demo.html'
    else:
        return 'patients/patient_detail_demo.html'
