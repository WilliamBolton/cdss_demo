from django.utils import timezone
from .models import PageVisit

'''class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Record page visit
            page_name = request.path  # You may want to customize this based on your needs
            PageVisit.objects.create(user=request.user, page_name=page_name)

        return response
'''
class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_page_visit = None  # Store the last recorded page visit

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            page_name = request.path

            # Check if it's a new page visit
            if not self.last_page_visit or self.last_page_visit.page_name != page_name:
                # Update exit timestamp for the previous page visit
                if self.last_page_visit:
                    self.last_page_visit.exit_timestamp = timezone.now()
                    self.last_page_visit.save()

                # Record entry timestamp for the new page visit
                self.last_page_visit = PageVisit.objects.create(user=request.user, page_name=page_name)

        return response
