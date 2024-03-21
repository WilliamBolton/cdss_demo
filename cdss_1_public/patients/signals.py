from django.utils import timezone
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.db.models.signals import Signal

@receiver(user_logged_out)
def record_logout_timestamp(sender, user, request, **kwargs):
    if user.is_authenticated:
        pass


@receiver(user_logged_out)
def handle_logout(sender, request, **kwargs):
    user = request.user

# Used for reseting all Patients form_filled_in attribute to False when a user logs out
# Note must be at bottom of script or get problems with timing data not being recorded
user_logged_out = Signal()