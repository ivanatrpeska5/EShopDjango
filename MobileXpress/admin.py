from django.contrib import admin
from .models import *


# Register your models here.

class PhoneColorInline(admin.TabularInline):
    model = PhoneColorQuantity
    extra = 0


class PhoneAdmin(admin.ModelAdmin):
    inlines = [PhoneColorInline]


admin.site.register(CustomUser)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Color)
admin.site.register(Manufacturer)
admin.site.register(CartItem)
admin.site.register(ShoppingCart)
admin.site.register(Order)
admin.site.register(Payment)
