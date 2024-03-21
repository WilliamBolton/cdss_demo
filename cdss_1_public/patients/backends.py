from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import UserProfile

class UserProfileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            # Try to find a user with the provided username (id in your case)
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None

        # Check if the user has a UserProfile
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None

        # Check if the provided password is valid
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None