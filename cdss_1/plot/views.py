from django.shortcuts import render
from .models import Vitals_plot

# Create your views here.
def vitals_plot_view(request):
    vitals_plot_data = Vitals_plot.objects.all()
    return render(request, 'plot/templates/index.html', {'vitals_plot_data': vitals_plot_data})