import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()

admin = User.objects.create_superuser('admin@admin.com', 'Hero Staff', 'pass')
admin.save()
