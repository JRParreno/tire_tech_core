# Generated by Django 4.2.2 on 2023-07-02 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_description', models.CharField(max_length=255)),
                ('walk_in_description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Service Information',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ServiceOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
                ('is_available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Service Offer',
                'verbose_name_plural': 'Services Offer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Shop Category',
                'verbose_name_plural': 'Shop Categories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=25)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('services_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_info', to='shop.serviceinfo')),
                ('shop_category', models.ManyToManyField(related_name='shop_categories', to='shop.shopcategory')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_shop', to='user_profile.userprofile')),
                ('vehicle_types', models.ManyToManyField(related_name='shop_vehicles', to='vehicle.vehicle')),
            ],
            options={
                'verbose_name': 'Shop',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='serviceinfo',
            name='services',
            field=models.ManyToManyField(related_name='services_offer', to='shop.serviceoffer'),
        ),
    ]
