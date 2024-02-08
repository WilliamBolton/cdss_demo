from django.urls import path

from . import views
from .views import vitals_plot_view

urlpatterns = [
    path('', vitals_plot_view, name='vitals_plot_view'),
]