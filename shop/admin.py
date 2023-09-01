from django.contrib import admin
from .models import Shop, ServiceOffer, ShopCategory, ShopPhotos, ProductOffer, ShopReview
from django_admin_geomap import ModelAdmin


admin.site.register(ShopReview)


class ShopPhotoTabularInLine(admin.TabularInline):
    model = ShopPhotos
    fields = ('shop', 'image')


class Admin(ModelAdmin):
    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"
    geomap_item_zoom = "15"
    geomap_show_map_on_list = False
    inlines = [ShopPhotoTabularInLine]
    list_display = ('id', 'shop_name',
                    'open_time', 'close_time',)
    ordering = ('shop_name',)
    search_fields = ('shop_name',)
    filter_horizontal = ('shop_category', 'vehicle_types',
                         'products', 'services')

    def get_queryset(self, request):
        qs = super(Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_profile__user=request.user)


admin.site.register(Shop, Admin)


@admin.register(ServiceOffer)
class ServiceOfferAdminView(admin.ModelAdmin):
    list_display = ('id', 'service_name')
    ordering = ('service_name',)
    search_fields = ('service_name',)

    def get_queryset(self, request):
        qs = super(ServiceOfferAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_profile__user=request.user)


@admin.register(ShopCategory)
class ShopCategorypAdminView(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    ordering = ('category_name',)
    search_fields = ('category_name',)


@admin.register(ProductOffer)
class ProductOfferAdminView(admin.ModelAdmin):
    list_display = ('id', 'product_name',)
    ordering = ('product_name',)
    search_fields = ('product_name',)

    def get_queryset(self, request):
        qs = super(ProductOfferAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_profile__user=request.user)
