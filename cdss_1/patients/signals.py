from django.utils import timezone
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import PageVisit, LinkClick, HoverEvent
import csv
from io import StringIO
import os
from django.db.models.signals import Signal

@receiver(user_logged_out)
def record_logout_timestamp(sender, user, request, **kwargs):
    if user.is_authenticated:
        # Find the last recorded page visit for the user
        last_page_visit = PageVisit.objects.filter(user=user).order_by('-entry_timestamp').first()

        # Update the exit timestamp for each page visit
        if last_page_visit:
            last_page_visit.exit_timestamp = timezone.now()
            last_page_visit.save()

@receiver(user_logged_out)
def handle_logout(sender, request, **kwargs):
    user = request.user
    page_visits = PageVisit.objects.filter(user=user)
    link_clicks = LinkClick.objects.filter(user=user)
    hover_events = HoverEvent.objects.filter(user=user)
    
    print('page_visits len:', len(page_visits))
    print('link_clicks len:', len(link_clicks))
    print('hover_events len:', len(hover_events))

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
    
    # Create a CSV string for hover events
    csv_data3 = StringIO()
    csv_writer3 = csv.writer(csv_data3)
    csv_writer3.writerow(['user_id', 'user_archetype', 'patient', 'component', 'hover_duration'])

    for event in hover_events:
        patient_id = event.patient_id
        patient_id = patient_id.lstrip('Patient ') # Strip to just return number in string form
        csv_writer3.writerow([user_id, user_archetype, patient_id, event.component, event.hover_duration])

    # Save CSV data to a file in the 'click_results' folder
    csv_file_path3 = f'/home/wb1115/VSCode_projects/cdss/cdss_1/cdss_1/hover_results/{user_id}_hover_events.csv'

    with open(csv_file_path3, 'w') as csv_file3:
        csv_file3.write(csv_data3.getvalue())

# Used for reseting all Patients form_filled_in attribute to False when a user logs out
# Note must be at bottom of script or get problems with timing data not being recorded
user_logged_out = Signal()