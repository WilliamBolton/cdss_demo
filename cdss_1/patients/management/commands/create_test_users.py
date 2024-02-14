from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from patients.models import UserProfile

def create_test_user_profiles():
    # Create UserProfiles
    for x in range(11): #101
        username = str(x)
        archetype = 'b' if x % 2 else 'a'

        # Check if the user with the given username already exists
        if not User.objects.filter(username=username).exists():
            # Create the user and user profile
            test_user = User.objects.create_user(username=username, password='test_password')
            UserProfile.objects.create(user=test_user, id_value=username, archetype=archetype)
            # Currently have users up to 100 with alternating a and b

class Command(BaseCommand):
    help = 'Remove all users and create new test users'

    def handle(self, *args, **options):
        # Delete all existing users
        #User.objects.all().delete()

        # Create new test users
        create_test_user_profiles()

        self.stdout.write(self.style.SUCCESS('Successfully created test users'))
    
        print_bool = False
        #print_bool = True
        if print_bool == True:
            # Retrieve all UserProfile instances
            user_profiles = UserProfile.objects.all()
            # Print or iterate over the user profiles
            for user_profile in user_profiles:
                print(user_profile.id_value, user_profile.archetype)
            print('\n\n\n\n\n')
        print('\n ##### \n\n\n Completed loading \n\n\n ##### \n')


# python manage.py create_test_users
    
