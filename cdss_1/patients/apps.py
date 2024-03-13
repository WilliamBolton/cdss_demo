import os
import sys
from django.apps import AppConfig
from django.db.models.signals import post_migrate

def age_fun(n):
    if n == 'Patient 1':
        return '65'
    elif n == 'Patient 2':
        return '25'
    elif n == 'Patient 7':
        return '91'
    elif n == 'Patient 8':
        return '57'
    elif n == 'Patient 9':
        return '57'
    elif n == 'Patient 10':
        return '83'
    elif n == 'Patient 11':
        return '70'
    elif n == 'Patient 12':
        return '61'
    else:
        return 'nan'

def sex_fun(n):
    if n == 'Patient 1':
        return 'Male'
    elif n == 'Patient 2':
        return 'Female'
    elif n == 'Patient 7':
        return 'Male'
    elif n == 'Patient 8':
        return 'Male'
    elif n == 'Patient 9':
        return 'Female'
    elif n == 'Patient 10':
        return 'Female'
    elif n == 'Patient 11':
        return 'Male'
    elif n == 'Patient 12':
        return 'Female'
    else:
        return 'nan'

def ethnicity_fun(n):
    if n == 'Patient 1':
        return 'White'
    elif n == 'Patient 2':
        return 'Female'
    elif n == 'Patient 7':
        return 'White'
    elif n == 'Patient 8':
        return 'Native American'
    elif n == 'Patient 9':
        return 'White'
    elif n == 'Patient 10':
        return 'White'
    elif n == 'Patient 11':
        return 'White'
    elif n == 'Patient 12':
        return 'White'
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
    elif n == 'Patient 7':
        return 'IV for 2 days'
    elif n == 'Patient 8':
        return 'IV for 6 days'
    elif n == 'Patient 9':
        return 'IV for 4 days'
    elif n == 'Patient 10':
        return 'IV for 2 days'
    elif n == 'Patient 11':
        return 'IV for 2 days'
    elif n == 'Patient 12':
        return 'IV for 3 days'
    else:
        return 'nan'

def prediction_fun(n):
    if n == 'Patient 1':
        return 'Dont switch'
    elif n == 'Patient 2':
        return 'Switch'
    elif n == 'Patient 7':
        return 'Dont switch'
    elif n == 'Patient 8':
        return 'Switch'
    elif n == 'Patient 9':
        return 'Potentially switch'
    elif n == 'Patient 10':
        return 'Dont switch'
    elif n == 'Patient 11':
        return 'Switch'
    elif n == 'Patient 12':
        return 'Potentially switch'
    else:
        return 'nan'

def guideline_fun(n):
    if n == 'Patient 1':
        return 'Reassess in 24 hours'
    elif n == 'Patient 2':
        return 'Switch'
    elif n == 'Patient 7':
        return 'Reassess in 24 hours'
    elif n == 'Patient 8':
        return 'Prompt or assess for switch'
    elif n == 'Patient 9':
        return 'Prompt or assess for switch'
    elif n == 'Patient 10':
        return 'Prompt or assess for switch'
    elif n == 'Patient 11':
        return 'Reassess in 24 hours'
    elif n == 'Patient 12':
        return 'Reassess in 24 hours'
    else:
        return 'nan'

def create_initial_patients(sender, **kwargs):
    from .models import Patient

    # Check if there are no patients in the database - remove this or wont run new each time
    #if not Patient.objects.exists():
    # Remove current patients
    Patient.objects.all().delete()
    # Create patients (10)
    for i in range(1, 13): #11 #3
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

def imddecil_fun_demo(n):
    if n == 'Patient 1':
        return '3'
    elif n == 'Patient 2':
        return '7'
    else:
        return 'nan'

def comorbidities_fun_demo(n):
    if n == 'Patient 1':
        return 'Diabetes'
    elif n == 'Patient 2':
        return 'Obesity'
    else:
        return 'nan'
    
def diagosis_fun_demo(n):
    if n == 'Patient 1':
        return 'Pneumonia'
    elif n == 'Patient 2':
        return 'Urinary tract infection'
    else:
        return 'nan'
    
def antibiotic_fun_demo(n):
    if n == 'Patient 1':
        return 'IV co-amoxiclav for 2 days'
    elif n == 'Patient 2':
        return 'IV xxx for 2 days'
    elif n == 'Patient 3':
        return 'IV for 3 days'
    else:
        return 'nan'

def prediction_fun_demo(n):
    if n == 'Patient 1':
        return 'Dont switch'
    elif n == 'Patient 2':
        return 'Switch'
    elif n == 'Patient 3':
        return 'Potentially switch'
    else:
        return 'nan'

def guideline_fun_demo(n):
    if n == 'Patient 1':
        return 'Reassess in 24 hours'
    elif n == 'Patient 2':
        return 'Switch'
    elif n == 'Patient 3':
        return 'Reassess in 24 hours'
    else:
        return 'nan'

def create_initial_demo_patients(sender, **kwargs):
    from .models import Patient_demo

    # Check if there are no patients in the database - remove this or wont run new each time
    #if not Patient.objects.exists():
    # Remove current patients
    Patient_demo.objects.all().delete()
    # Create patients (10)
    for i in range(1, 4):
        # Define name
        patient_demo = Patient_demo.objects.create(name=f"Patient {i}")
        print(patient_demo.name)

        # Define csv_path
        # Assume CSV files are in the 'csv' directory
        csv_file_path = os.path.join('csv/vitals', f'patient_{i}_demo.csv')
        #print('csv_file_path', csv_file_path)
        if os.path.exists(csv_file_path):
            patient_demo.vitals_csv_path = csv_file_path
            patient_demo.save()

        # Define patients_csv_path
        csv_file_path = os.path.join('csv/patient', f'patient_{i}_demo.csv')
        if os.path.exists(csv_file_path):
            patient_demo.patient_csv_path = csv_file_path
            patient_demo.save()

        # Define similar_patients_csv_path
        csv_file_path = os.path.join('csv/similar', f'patient_{i}_demo.csv')
        if os.path.exists(csv_file_path):
            patient_demo.similar_patients_csv_path = csv_file_path
            patient_demo.save()
        
        # Define similar_patients_csv_path
        png_file_path = os.path.join('images', f'patient_{i}_demo_feature_similarity.png')
        if os.path.exists(png_file_path):
            patient_demo.feature_similarity_path = png_file_path
            patient_demo.save()

        # Define age
        patient_demo.age = age_fun(patient_demo.name)
        patient_demo.save()
            
        # Define sex
        patient_demo.sex = sex_fun(patient_demo.name)
        patient_demo.save()

        # Define ethnicity
        patient_demo.ethnicity = ethnicity_fun(patient_demo.name)
        patient_demo.save()

        # Define imddecil
        patient_demo.imddecil = imddecil_fun_demo(patient_demo.name)
        patient_demo.save()

        # Define comorbidities
        patient_demo.comorbidities = comorbidities_fun_demo(patient_demo.name)
        patient_demo.save()
            
        # Define diagnosis
        patient_demo.diagnosis = diagosis_fun_demo(patient_demo.name)
        patient_demo.save()
            
        # Define antibiotics
        patient_demo.antibiotic = antibiotic_fun_demo(patient_demo.name)
        patient_demo.save()

        # Define prediction
        patient_demo.prediction = prediction_fun_demo(patient_demo.name)
        patient_demo.save()

        # Define guidelines
        patient_demo.guideline = guideline_fun_demo(patient_demo.name)
        patient_demo.save()
        
class PatientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patients'

    def ready(self):
        import patients.signals
        import patients.receivers

        if 'runserver' not in sys.argv:
            return True
        
        # Connect the create_initial_patients function to the post_migrate signal        
        #post_migrate.connect(create_initial_patients, sender=self)
        
        create_initial_patients(self)
        print('Demo')
        create_initial_demo_patients(self)
