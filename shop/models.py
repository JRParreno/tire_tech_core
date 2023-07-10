from django.db import models
from user_profile.models import UserProfile
from vehicle.models import Vehicle

class ShopCategory(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
       return f'{self.category_name}'

    class Meta:
        managed = True
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'


class ServiceOffer(models.Model):
    service_name = models.CharField(max_length=255)

    def __str__(self):
        return self.service_name

    class Meta:
        managed = True
        verbose_name = 'Service Offer'
        verbose_name_plural = 'Services Offer'


class ServiceInfo(models.Model):
    service_description = models.CharField(max_length=255)
    walk_in_description = models.CharField(max_length=255)
    services = models.ManyToManyField(ServiceOffer, related_name='services_offer')

    def __str__(self):
        return f'{self.service_description}'

    class Meta:
        managed = True
        verbose_name = 'Service Information'


class ProductOffer(models.Model):
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return self.service_name

    class Meta:
        managed = True
        verbose_name = 'Product Offer'
        verbose_name_plural = 'Products Offer'


class ProductInfo(models.Model):
    service_description = models.CharField(max_length=255)
    walk_in_description = models.CharField(max_length=255)
    products = models.ManyToManyField(ProductOffer, related_name='products_offer')

    def __str__(self):
        return f'{self.service_description}'

    class Meta:
        managed = True
        verbose_name = 'Product Information'


class Shop(models.Model):
    user_profile = models.OneToOneField(UserProfile, related_name='user_shop', on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=25)
    open_time = models.TimeField()
    close_time = models.TimeField()
    special_offers = models.TextField(blank=True)
    address_name = models.CharField(max_length=255)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    services_info = models.ForeignKey(
        ServiceInfo, related_name='services_info', on_delete=models.CASCADE)
    vehicle_types = models.ManyToManyField(Vehicle, related_name='shop_vehicles')
    shop_category = models.ManyToManyField(ShopCategory, related_name='shop_categories')
    
    def __str__(self):
        return f'{self.shop_name}- {self.address.address_name}'
    
    class Meta:
        managed = True
        verbose_name = 'Shop'


class ShopPhotos(models.Model):
    shop = models.ForeignKey(Shop, related_name='shop_photos', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='shop-pictures/', blank=True, null=True)



