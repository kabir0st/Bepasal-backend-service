import os

from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from faker import Faker

from core.utils.functions import client_has_app
from tenants.models import Client
from users.models.users import UserBase

fake = Faker()


class Command(BaseCommand):
    help = 'Populate dummy users'
    max_users = 100

    def handle(self, *args, **kwargs):
        if os.environ.get("GITHUB_WORKFLOW"):
            self.max_users = 1
        for client in Client.objects.filter():
            with tenant_context(client):
                if client_has_app('ecommerce'):
                    self.populate_users()

    def populate_users(self):
        print(f"Populating Users: {self.max_users}")
        for _ in range(self.max_users):
            UserBase.objects.create(
                email=fake.email(),
                given_name=fake.first_name(),
                family_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                zip_code=fake.zipcode(),
                city=fake.city(),
                country=fake.country(),
                is_verified=True,  # Assuming all users are verified
                is_staff=False,
                is_active=True,
            )
