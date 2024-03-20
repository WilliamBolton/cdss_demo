from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from patients.models import Patient

@receiver(user_logged_out)
def handle_logout(sender, request, **kwargs):
    # Set form_filled_in to False for all patients
    Patient.objects.all().update(form_filled_in=False)
