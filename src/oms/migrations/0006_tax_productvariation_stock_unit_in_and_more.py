# Generated by Django 4.2 on 2023-12-27 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0005_remove_productvariation_is_default_variation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('rate_type', models.CharField(choices=[('fixed', 'fixed'), ('percent', 'percent')], default='percent', max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='productvariation',
            name='stock_unit_in',
            field=models.CharField(choices=[('unit', 'unit'), ('kg', 'kg'), ('g', 'g'), ('l', 'l'), ('ml', 'ml')], default='g', max_length=25),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='tax_type',
            field=models.CharField(choices=[('exclusive', 'exclusive'), ('inclusive', 'inclusive')], default='exclusive', max_length=25),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=60),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='crossed_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=60),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=60),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='stock',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=60),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='taxes_applied',
            field=models.ManyToManyField(blank=True, to='oms.tax'),
        ),
    ]