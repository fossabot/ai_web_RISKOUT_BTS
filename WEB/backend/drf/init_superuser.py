import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf.settings");
DJANGO_DB_NAME = os.environ['DJANGO_DB_NAME']
DJANGO_SU_NAME = os.environ['DJANGO_SU_NAME']
DJANGO_SU_EMAIL = os.environ['DJANGO_SU_EMAIL']
DJANGO_SU_PASSWORD = os.environ['DJANGO_SU_PASSWORD']

import django;
django.setup();

from django.contrib.auth.management.commands.createsuperuser import get_user_model;
get_user_model()._default_manager.db_manager(DJANGO_DB_NAME).create_superuser(username=DJANGO_SU_NAME,email=DJANGO_SU_EMAIL,password=DJANGO_SU_PASSWORD)
