from django.urls import path

from . import views
from .views import vitals_table_view

#urlpatterns = [
#    path("", views.index, name="index"),
#]

urlpatterns = [
    path('', vitals_table_view, name='vitals_table_view'),
]