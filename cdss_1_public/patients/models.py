from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
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
    form_filled_in = models.BooleanField(default=False)

class Patient_demo(models.Model):
    name = models.CharField(max_length=100)
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
    form_filled_in = models.BooleanField(default=False)

class DecisionPoint(models.Model): # I think this can be removed
    label = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.label

class Answer(models.Model):
    decision_point = models.ForeignKey(DecisionPoint, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    style = models.CharField(max_length=50, choices=[('success', 'Success'), ('danger', 'Danger'), ('info', 'Info'), ('warning', 'Warning')])
    bg_class = models.CharField(max_length=50, default='bg-light')
    text_class = models.CharField(max_length=50, default='text-dark')

    def __str__(self):
        return self.text

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    id_value = models.CharField(max_length=50)
    archetype = models.CharField(max_length=50)

    def __str__(self):
        return f"username: {self.user.username}, id_value: {self.id_value}, archetype: {self.archetype}"