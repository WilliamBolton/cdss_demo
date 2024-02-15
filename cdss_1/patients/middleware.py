from django.utils import timezone
from .models import PageVisit

class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Record page visit
            page_name = request.path  # You may want to customize this based on your needs
            PageVisit.objects.create(user=request.user, page_name=page_name)

        return response