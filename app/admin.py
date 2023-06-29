from django.contrib import admin
from .models import Package

# Register your models here.
class PackageAdmin(admin.ModelAdmin):
    model = Package
    list_display = ['senderName', 'senderEmail', 'senderPhone', 'senderAddress', 'recipeintName', 'recipeintPhone', 'recipeintAddress', 'additionalComment', 'product', 'tracking_id', 'weight', 'height', 'delivery_location', 'status', 'created_at']

admin.site.register(Package, PackageAdmin)