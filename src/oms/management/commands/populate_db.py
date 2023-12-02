import random
from django.core.management.base import BaseCommand
from faker import Faker
from core.utils.functions import client_has_app
from oms.models import (Category, VariationType,
                        VariationOption, Product, ProductVariation)
from tenants.models import Client
from django_tenants.utils import tenant_context
from django.db import transaction
fake = Faker()


class Command(BaseCommand):
    help = 'Populate dummy data for testing'

    def handle(self, *args, **kwargs):
        for client in Client.objects.filter():
            with tenant_context(client):
                if client_has_app('oms'):
                    self.populate_categories()
                    self.populate_variation_types()
                    self.populate_products()

    def populate_categories(self):
        for i in range(10):
            Category.objects.create(
                name=f"{fake.word()} {i}",
                description=fake.text(),
            )

    def populate_variation_types(self):
        variations = {
            'Size': ['SM', 'M', 'L', 'X', 'XL', 'XXL'],
            'Color': ["Red", "Green", "Blue", "Yellow", "Orange",
                      "Purple", "Pink", "Brown", "Cyan", "Magenta"],
            'Cloth': ['Cotton', 'Linen', 'Polyester']
        }
        for variation in variations:
            variation_type = VariationType.objects.create(name=variation)
            for option in variations[variation]:
                VariationOption.objects.create(
                    name=option,
                    variation_type=variation_type,
                )

    def populate_products(self):
        categories = Category.objects.all()
        variation_types = VariationType.objects.all()

        for i in range(100):
            with transaction.atomic():
                applied_variation_combinations = []
                product = Product.objects.create(
                    name=f"{fake.word()} {i}",
                    description=fake.text(),
                    thumbnail_image=fake.image_url(),
                )
                product.categories.set(random.sample(
                    list(categories), random.randint(1, 5)))
                product.enabled_variation_types.set(random.sample(
                    list(variation_types), random.randint(1, 3)))

                for _ in range(8):
                    variation_option_combination = []
                    for variation_type in (
                            product.enabled_variation_types.filter(
                            )):
                        variation_option_combination.append(
                            random.choice(
                                list(variation_type.options.filter()))
                        )
                    if variation_option_combination not in (
                            applied_variation_combinations):
                        ProductVariation.objects.create(
                            product=product,
                            selling_price=fake.random_int(min=10, max=100),
                            crossed_price=fake.random_int(min=10, max=100),
                            cost_price=fake.random_int(min=5, max=50),
                            quantity=fake.random_int(min=1, max=100),
                            sku=fake.word(),
                            is_eligible_for_discount=fake.boolean(),
                        ).variation_option_combination.set(
                            variation_option_combination)
                        applied_variation_combinations.append(
                            variation_option_combination)
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully populated product: {product}'))
