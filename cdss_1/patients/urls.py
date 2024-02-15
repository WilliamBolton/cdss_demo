from django.urls import path
from .views import login_view, patient_list, patient_detail, prediction_page, guideline_page, process_user_input, logout_view, track_link_click

urlpatterns = [
    #path('login/', LoginView.as_view(), name='login'),
    path('', login_view, name='login'),
    path('patients', patient_list, name='patient_list'),
    path('<int:patient_id>/', patient_detail, name='patient_detail'),
    path('<int:patient_id>/prediction/', prediction_page, name='prediction_page'),
    path('<int:patient_id>/guideline/', guideline_page, name='guideline_page'),
    path('<int:patient_id>/process_user_input/', process_user_input, name='process_user_input'),
    #path('<int:patient_id>/simple/', patient_detail_simple, name='patient_detail_simple'),
    path('logout/', logout_view, name='logout'),
    path('track_link_click/', track_link_click, name='track_link_click'),
]