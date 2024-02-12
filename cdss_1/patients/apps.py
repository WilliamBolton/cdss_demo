import os
import sys
from django.apps import AppConfig
from django.db.models.signals import post_migrate

def age_fun(n):
    if n == 'Patient 1':
        return '65'
    elif n == 'Patient 2':
        return '25'
    else:
        return 'nan'

def sex_fun(n):
    if n == 'Patient 1':
        return 'Male'
    elif n == 'Patient 2':
        return 'Female'
    else:
        return 'nan'

def ethnicity_fun(n):
    if n == 'Patient 1':
        return 'White'
    elif n == 'Patient 2':
        return 'Female'
    else:
        return 'nan'

def imddecil_fun(n):
    if n == 'Patient 1':
        return '4'
    elif n == 'Patient 2':
        return 'xxx'
    else:
        return 'nan'

def comorbidities_fun(n):
    if n == 'Patient 1':
        return 'Obesity'
    elif n == 'Patient 2':
        return 'xxx'
    else:
        return 'nan'
    
def diagosis_fun(n):
    if n == 'Patient 1':
        return 'Pneumonia'
    elif n == 'Patient 2':
        return 'Uncomplicated urinary tract infection'
    else:
        return 'nan'
    
def antibiotic_fun(n):
    if n == 'Patient 1':
        return 'IV co-amoxiclav for 1 day'
    elif n == 'Patient 2':
        return 'IV xxx for 3 days'
    else:
        return 'nan'

def prediction_fun(n):
    if n == 'Patient 1':
        return 'Dont switch'
    elif n == 'Patient 2':
        return 'Switch'
    else:
        return 'nan'

def guideline_fun(n):
    if n == 'Patient 1':
        return 'Dont switch'
    elif n == 'Patient 2':
        return 'Switch'
    else:
        return 'nan'

def create_initial_patients(sender, **kwargs):
    from .models import Patient

    # Check if there are no patients in the database - remove this or wont run new each time
    #if not Patient.objects.exists():
    # Remove current patients
    Patient.objects.all().delete()
    # Create patients (10)
    for i in range(1, 11):
        # Define name
        patient = Patient.objects.create(name=f"Patient {i}")
        print(patient.name)

        # Define csv_path
        # Assume CSV files are in the 'csv' directory
        csv_file_path = os.path.join('csv/vitals', f'patient_{i}.csv')
        #print('csv_file_path', csv_file_path)
        if os.path.exists(csv_file_path):
            patient.vitals_csv_path = csv_file_path
            patient.save()
        
        # Define patients_csv_path
        csv_file_path = os.path.join('csv/patient', f'patient_{i}.csv')
        if os.path.exists(csv_file_path):
            patient.patient_csv_path = csv_file_path
            patient.save()

        # Define similar_patients_csv_path
        csv_file_path = os.path.join('csv/similar', f'patient_{i}.csv')
        if os.path.exists(csv_file_path):
            patient.similar_patients_csv_path = csv_file_path
            patient.save()
        
        # Define similar_patients_csv_path
        png_file_path = os.path.join('images', f'patient_{i}_feature_similarity.png')
        if os.path.exists(png_file_path):
            patient.feature_similarity_path = png_file_path
            patient.save()

        # Define age
        patient.age = age_fun(patient.name)
        patient.save()
            
        # Define sex
        patient.sex = sex_fun(patient.name)
        patient.save()

        # Define ethnicity
        patient.ethnicity = ethnicity_fun(patient.name)
        patient.save()

        # Define imddecil
        patient.imddecil = imddecil_fun(patient.name)
        patient.save()

        # Define comorbidities
        patient.comorbidities = comorbidities_fun(patient.name)
        patient.save()
            
        # Define diagnosis
        patient.diagnosis = diagosis_fun(patient.name)
        patient.save()
            
        # Define antibiotics
        patient.antibiotic = antibiotic_fun(patient.name)
        patient.save()

        # Define prediction
        patient.prediction = prediction_fun(patient.name)
        patient.save()

        # Define guidelines
        patient.guideline = guideline_fun(patient.name)
        patient.save()
        

class PatientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patients'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        
        # Connect the create_initial_patients function to the post_migrate signal        
        #post_migrate.connect(create_initial_patients, sender=self)
        create_initial_patients(self)
        