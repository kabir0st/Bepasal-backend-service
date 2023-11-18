# Generated by Django 4.2 on 2023-11-18 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0003_remove_itemvariation_variation_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemimage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='itemvariationimage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='variationoption',
            options={},
        ),
        migrations.AlterModelOptions(
            name='variationtype',
            options={},
        ),
        migrations.RemoveField(
            model_name='itemimage',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='itemimage',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='itemimage',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='itemvariationimage',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='itemvariationimage',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='itemvariationimage',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='variationoption',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='variationoption',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='variationoption',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='variationtype',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='variationtype',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='variationtype',
            name='updated_at',
        ),
    ]
