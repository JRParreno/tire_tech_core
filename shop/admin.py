from django.contrib import admin
from .models import Shop, ServiceOffer, ShopCategory, ShopPhotos, ProductOffer
from nested_admin.nested import NestedTabularInline, NestedStackedInline
from user_profile.models import UserProfile


class ShopPhotoTabularInLine(admin.TabularInline):
    model = ShopPhotos
    fields = ('shop', 'image')


@admin.register(Shop)
class ShopAdminView(admin.ModelAdmin):
    inlines = [ShopPhotoTabularInLine,]
    list_display = ('id', 'shop_name',
                    'open_time', 'close_time',)
    ordering = ('shop_name',)
    search_fields = ('shop_name',)
    filter_horizontal = ('shop_category', 'vehicle_types',
                         'products', 'services')

    def get_queryset(self, request):
        qs = super(ShopAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_profile__user=request.user)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "user_profile":
    #         kwargs["queryset"] = UserProfile.objects.filter(user=request.user)
    #     return super(ShopAdminView, self).formfield_for_foreignkey(db_field, request, **kwargs)


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
