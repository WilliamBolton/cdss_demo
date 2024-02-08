import os
#import sys
#from django.core.management import execute_from_command_line

def run():
    # Reset db
    os.system('rm db.sqlite3')
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')

    # Run the development server
    #execute_from_command_line(['manage.py', 'runserver'])
    os.system('python manage.py runserver --noreload')

if __name__ == '__main__':
    run()