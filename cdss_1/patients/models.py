from django.db import models
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
import os

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    #details = models.CharField(max_length=1000)
    #csv_file = models.FileField(upload_to='patient_csv/', blank=True, null=True)
    vitals_csv_path = models.CharField(max_length=100, default='nan')
    patient_csv_path = models.CharField(max_length=100, default='nan')
    similar_patients_csv_path = models.CharField(max_length=100, default='nan')
    feature_similarity_path = models.CharField(max_length=100, default='nan')
    age = models.CharField(max_length=100, default='nan')
    sex = models.CharField(max_length=100, default='nan')
    ethnicity = models.CharField(max_length=100, default='nan')
    imddecil = models.CharField(max_length=100, default='nan')
    comorbidities = models.CharField(max_length=100, default='nan')
    diagnosis = models.CharField(max_length=100, default='nan')
    antibiotic = models.CharField(max_length=100, default='nan')
    prediction = models.CharField(max_length=100, default='nan')
    guideline = models.CharField(max_length=100, default='nan')

'''@receiver(post_save, sender=Patient)
def set_default_csv_path(sender, instance, **kwargs):
    if instance.csv_path == 'nan':
        instance.csv_path = f'csv/patient_{instance.pk}.csv'
        instance.save()

def create_initial_patients(sender, **kwargs):
    from .models import Patient

    # Check if there are no patients in the database
    if not Patient.objects.exists():
        # Create 10 patients
        for i in range(1, 11):
            patient = Patient.objects.create(name=f"Patient {i}")'''

'''def create_initial_patients(sender, **kwargs):
    from .models import Patient

    # Check if there are no patients in the database
    if not Patient.objects.exists():
        # Create 10 patients
        for i in range(1, 20):
            patient = Patient.objects.create(name=f"Patient {i}")

            # Assuming CSV files are in the 'csv_files' directory
            csv_file_path = os.path.join('csv', f'patient_{i}.csv')
            print("----", csv_file_path)

            if os.path.exists(csv_file_path):
                patient.csv_path = csv_file_path
                patient.save()

post_migrate.connect(create_initial_patients, sender=Patient)'''