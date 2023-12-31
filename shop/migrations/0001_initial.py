# Generated by Django 4.2.2 on 2023-07-15 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Product Offer',
                'verbose_name_plural': 'Products Offer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ServiceOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Service Offer',
                'verbose_name_plural': 'Services Offer',
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
                ('special_offers', models.TextField(blank=True)),
                ('address_name', models.CharField(max_length=255)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('service_description', models.CharField(max_length=255)),
                ('walk_in_service_description', models.CharField(max_length=255)),
                ('product_description', models.CharField(max_length=255)),
                ('walk_in_product_description', models.CharField(max_length=255)),
                ('products', models.ManyToManyField(related_name='products_offer', to='shop.productoffer')),
                ('services', models.ManyToManyField(related_name='services_offer', to='shop.serviceoffer')),
            ],
            options={
                'verbose_name': 'Shop',
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
            name='ShopPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='shop-pictures/')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_photos', to='shop.shop')),
            ],
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_category',
            field=models.ManyToManyField(related_name='shop_categories', to='shop.shopcategory'),
        ),
        migrations.AddField(
            model_name='shop',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_shop', to='user_profile.userprofile'),
        ),
        migrations.AddField(
            model_name='shop',
            name='vehicle_types',
            field=models.ManyToManyField(related_name='shop_vehicles', to='vehicle.vehicle'),
        ),
    ]
