from django.urls import path
from .views import guideline_page_demo, login_view, patient_detail_demo, patient_list, patient_detail, patient_list_demo, prediction_page, guideline_page, prediction_page_demo, process_user_input, logout_view, process_user_input_demo, thank_you

urlpatterns = [
    path('', login_view, name='login'),
    path('patients', patient_list, name='patient_list'),
    path('patients_demo', patient_list_demo, name='patient_list_demo'),
    path('<int:patient_id>/', patient_detail, name='patient_detail'),
    path('<int:patient_id>_demo/', patient_detail_demo, name='patient_detail_demo'),
    path('<int:patient_id>/prediction/', prediction_page, name='prediction_page'),
    path('<int:patient_id>_demo/prediction/', prediction_page_demo, name='prediction_page_demo'),   
    path('<int:patient_id>/guideline/', guideline_page, name='guideline_page'),
    path('<int:patient_id>_demo/guideline/', guideline_page_demo, name='guideline_page_demo'),
    path('<int:patient_id>/process_user_input/', process_user_input, name='process_user_input'),
    path('<int:patient_id>/process_user_input_demo/', process_user_input_demo, name='process_user_input_demo'),
    path('logout/', logout_view, name='logout'),
    path('thank_you', thank_you, name='thank_you'),
]