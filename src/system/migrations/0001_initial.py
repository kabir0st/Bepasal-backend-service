# Generated by Django 5.0.6 on 2024-06-29 18:47

import core.utils.functions
import django.db.models.deletion
import system.models.product
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['-is_active', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FonePayPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qr_status', models.CharField(choices=[('initiated', 'initiated'), ('requested', 'requested'), ('failed', 'failed'), ('success', 'success')], default='initiated', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('last_response_from_fonepay', models.TextField(blank=True, null=True)),
                ('invoice_number', models.CharField(max_length=255)),
                ('is_verified_from_server', models.BooleanField(default=False)),
                ('trace_id', models.TextField(blank=True, default='', null=True)),
                ('ird_details_sent', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-is_active', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(max_length=255)),
                ('variation', models.CharField(max_length=255)),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('discount_remarks', models.CharField(default='', max_length=255)),
                ('bill_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('is_refunded', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('cancelled_remarks', models.TextField(blank=True, default='')),
                ('returned_remarks', models.TextField(blank=True, default='')),
                ('refunded_remarks', models.TextField(blank=True, default='')),
            ],
            options={
                'ordering': ['-is_active', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItemStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('subtract_from_inventory', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-is_active', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('subtract_from_inventory', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-is_active', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_type', models.CharField(choices=[('fonepay', 'Fonepay'), ('staff_approved', 'Staff Approved')], default='fonepay', max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('remarks', models.TextField(blank=True, default='')),
                ('is_refunded', models.BooleanField(default=False)),
                ('refunded_remarks', models.TextField(blank=True, default='')),
            ],
            options={
                'ordering': ['-is_active', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('thumbnail_image', models.ImageField(blank=True, null=True, upload_to=system.models.product.image_directory_path)),
                ('continue_selling_after_out_of_stock', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=system.models.product.image_directory_path2)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('crossed_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('cost_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('stock', models.PositiveBigIntegerField(default=0)),
                ('sku', models.CharField(default='', max_length=255)),
                ('is_eligible_for_discount', models.BooleanField(default=True)),
                ('tax_type', models.CharField(choices=[('exclusive', 'exclusive'), ('inclusive', 'inclusive')], default='exclusive', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('thumbnail_image', models.ImageField(blank=True, null=True, upload_to=system.models.product.image_directory_path2)),
                ('is_eligible_for_discounts', models.BooleanField(default=True)),
                ('is_digital', models.BooleanField(default=False)),
                ('auto_complete_digital_orders', models.BooleanField(default=True)),
                ('digital_file', models.FileField(blank=True, null=True, upload_to=system.models.product.file_directory_path)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductVariationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=system.models.product.image_directory_path3)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('rate_type', models.CharField(choices=[('fixed', 'fixed'), ('percent', 'percent')], default='percent', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='VariationOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='VariationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='system.category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(blank=True, default='', max_length=255)),
                ('user_contact', models.CharField(blank=True, default='', max_length=255)),
                ('backup_contact', models.CharField(blank=True, default='', max_length=255)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('total_discount_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('extra_discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('discount_remarks', models.CharField(default='', max_length=255)),
                ('total_bill_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('total_amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('is_refunded', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('cancellation_remarks', models.TextField(blank=True, default='')),
                ('refunded_remarks', models.TextField(blank=True, default='')),
                ('extra_fields', models.JSONField(default=core.utils.functions.default_json)),
                ('delivery_note', models.CharField(blank=True, default='', max_length=255)),
                ('delivery_location', models.CharField(blank=True, default='', max_length=255)),
                ('geo_tag', models.JSONField(blank=True, default=core.utils.functions.default_json)),
                ('delivery_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.deliverymethod')),
            ],
            options={
                'ordering': ['-is_active', '-id'],
                'abstract': False,
            },
        ),
    ]
