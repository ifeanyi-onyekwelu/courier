from django.contrib import admin
from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    model = Coupon
    list_display = ['code', 'created_at', 'is_used', 'is_expired']

admin.site.register(Coupon, CouponAdmin)