import random

from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from faker import Faker

from core.utils.functions import client_has_app
from ecommerce.models.ecom import Review
from oms.models import (Product, )
from tenants.models import Client

fake = Faker()


class Command(BaseCommand):
    help = 'Populate dummy data for testing'

    def handle(self, *args, **kwargs):
        for client in Client.objects.filter():
            with tenant_context(client):
                if client_has_app('ecommerce'):
                    self.populate_reviews()

    def populate_reviews(self):
        for product in Product.objects.filter():
            for _ in range(random.randint(0, 20)):
                Review.objects.create(
                    user=None,
                    name=fake.name(),
                    product=product,
                    comment=fake.text(),
                    rating=random.randint(1, 10),
                )
