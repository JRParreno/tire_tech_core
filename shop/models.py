from django.db import models
from user_profile.models import UserProfile
from vehicle.models import Vehicle
from django_admin_geomap import GeoItem


class ProductOffer(models.Model):
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name

    class Meta:
        managed = True
        verbose_name = 'Product Offer'
        verbose_name_plural = 'Products Offer'


class ServiceOffer(models.Model):
    service_name = models.CharField(max_length=255)

    def __str__(self):
        return self.service_name

    class Meta:
        managed = True
        verbose_name = 'Service Offer'
        verbose_name_plural = 'Services Offer'


class ShopCategory(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        managed = True
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'


class Shop(models.Model, GeoItem):

    user_profile = models.OneToOneField(
        UserProfile, related_name='user_shop', on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=25)
    open_time = models.TimeField()
    close_time = models.TimeField()
    special_offers = models.TextField(blank=True)
    address_name = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    vehicle_types = models.ManyToManyField(
        Vehicle, related_name='shop_vehicles')
    shop_category = models.ManyToManyField(
        ShopCategory, related_name='shop_categories')
    service_description = models.CharField(max_length=255)
    walk_in_service_description = models.CharField(max_length=255)
    services = models.ManyToManyField(
        ServiceOffer, related_name='services_offer')
    product_description = models.CharField(
        max_length=255, null=True, blank=True)
    walk_in_product_description = models.CharField(
        max_length=255, null=True, blank=True)
    products = models.ManyToManyField(
        ProductOffer, related_name='products_offer', blank=True)

    def __str__(self):
        return f'{self.shop_name}- {self.address_name}'

    @property
    def geomap_longitude(self):
        return '' if self.longitude is None else str(self.longitude)

    @property
    def geomap_latitude(self):
        return '' if self.latitude is None else str(self.latitude)

    @property
    def geomap_popup_view(self):
        return "<strong>{}</strong>".format(str(self))

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view

    @property
    def geomap_popup_common(self):
        return self.geomap_popup_view

    class Meta:
        managed = True
        verbose_name = 'Shop'


class ShopPhotos(models.Model):
    shop = models.ForeignKey(
        Shop, related_name='shop_photos', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='shop-pictures/', blank=True, null=True)


class ShopReview(models.Model):
    shop = models.ForeignKey(
        Shop, related_name='shop_review', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(
        UserProfile, related_name='user_shop_review', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    rate = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_profile.user}'

    class Meta:
        managed = True
        verbose_name = 'ShopReview'
        verbose_name_plural = 'ShopReviews'
