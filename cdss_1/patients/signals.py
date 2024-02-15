from django.utils import timezone
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import PageVisit, LinkClick
import csv
from io import StringIO
import os


@receiver(user_logged_out)
def record_logout_timestamp(sender, user, request, **kwargs):
    if user.is_authenticated:
        # Find all page visits for the user
        page_visits = PageVisit.objects.filter(user=user)

        # Update the exit timestamp for each page visit
        for visit in page_visits:
            visit.exit_timestamp = timezone.now()
            visit.save()

@receiver(user_logged_out)
def handle_logout(sender, request, **kwargs):
    user = request.user
    page_visits = PageVisit.objects.filter(user=user)
    link_clicks = LinkClick.objects.filter(user=user)

    #print('page_visits:', page_visits)
    #print('link_clicks:', link_clicks)

    # Accessing the logged-in user's UserProfile
    user_profile = request.user.userprofile
    user_archetype = user_profile.archetype
    user_id = user_profile.id_value

    # Create a CSV string for page visits
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['user_id', 'user_archetype', 'page_name', 'entry_time', 'exit_time'])

    for visit in page_visits:
        csv_writer.writerow([user_id, user_archetype, visit.page_name, visit.entry_timestamp, visit.exit_timestamp])

    # Save CSV data to a file in the 'timing_results' folder
    csv_file_path = f'/home/wb1115/VSCode_projects/cdss/cdss_1/cdss_1/timing_results/{user_id}_page_visits.csv'

    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_data.getvalue())
    
    # Create a CSV string for link clicks 
    csv_data2 = StringIO()
    csv_writer2 = csv.writer(csv_data2)
    csv_writer2.writerow(['user_id', 'user_archetype', 'patient', 'link_clicks', 'timestamp'])

    for click in link_clicks:
        patient_id = click.patient_id
        patient_id = patient_id.lstrip('Patient ') # Strip to just return number in string form
        csv_writer2.writerow([user_id, user_archetype, patient_id, click.link_id, click.timestamp])

    # Save CSV data to a file in the 'click_results' folder
    csv_file_path2 = f'/home/wb1115/VSCode_projects/cdss/cdss_1/cdss_1/click_results/{user_id}_clicks.csv'

    with open(csv_file_path2, 'w') as csv_file2:
        csv_file2.write(csv_data2.getvalue())