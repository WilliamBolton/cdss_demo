from django.urls import path
from .views import patient_list, patient_detail, prediction_page, guideline_page, process_user_input

urlpatterns = [
    path('', patient_list, name='patient_list'),
    path('<int:patient_id>/', patient_detail, name='patient_detail'),
    path('<int:patient_id>/prediction/', prediction_page, name='prediction_page'),
    path('<int:patient_id>/guideline/', guideline_page, name='guideline_page'),
    path('<int:patient_id>/process_user_input/', process_user_input, name='process_user_input'),
]