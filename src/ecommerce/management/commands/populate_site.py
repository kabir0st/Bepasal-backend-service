import os
import random

from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from faker import Faker

from core.utils.functions import client_has_app
from ecommerce.models.ecom import QA, Review
from oms.models import Product
from tenants.models import Client

fake = Faker()


class Command(BaseCommand):
    help = 'Populate dummy data for testing'
    max_reviews = 100
    max_qas = 20

    def handle(self, *args, **kwargs):

        if os.environ.get("GITHUB_WORKFLOW"):
            self.max_reviews = 1
            self.max_qas = 1
        for client in Client.objects.filter():
            with tenant_context(client):
                if client_has_app('ecommerce'):
                    self.populate_reviews()
                    self.populate_qas()

    def populate_reviews(self):
        print('Populating Reviews . . .')
        for product in Product.objects.filter():
            for _ in range(random.randint(0, self.max_reviews)):
                Review.objects.create(
                    user=None,
                    name=fake.name(),
                    product=product,
                    comment=fake.text(),
                    rating=random.randint(1, 10),
                )

    def populate_qas(self):
        print('Populating QAs . . .')
        for product in Product.objects.filter():
            for _ in range(random.randint(0, self.max_qas)):
                QA.objects.create(
                    user=None,
                    name=fake.name(),
                    product=product,
                    question=fake.text(),
                    answer=fake.text()
                )
